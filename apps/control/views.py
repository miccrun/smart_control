
import json
import datetime

from astral import Astral

from django import http
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import (
    View,
    TemplateView,
)

#from apps.auth.views import LoginRequiredMixin

import apps.control as control_constants
from apps.control.models import (
    Room,
    Device,
    DeviceStatus,
    Config,
)


sunset_minus = None
sunset = None
sunrise = None
sunrise_plus = None
last_update = None


def update_sun():
    global sunset_minus, sunset, sunrise, sunrise_plus, last_update
    sunset_minus = city.sun(datetime.datetime.now() - datetime.timedelta(days=1))["sunset"].astimezone(
        timezone.get_default_timezone()).replace(tzinfo=None)
    sunset = city.sun(datetime.datetime.now())["sunset"].astimezone(
        timezone.get_default_timezone()).replace(tzinfo=None)
    sunrise = city.sun(datetime.datetime.now())["sunrise"].astimezone(
        timezone.get_default_timezone()).replace(tzinfo=None)
    sunrise_plus = city.sun(datetime.datetime.now() + datetime.timedelta(days=1))["sunrise"].astimezone(
        timezone.get_default_timezone()).replace(tzinfo=None)
    last_update = datetime.datetime.now()


city = Astral()["Chicago"]
update_sun()


class JSONResponseMixin(object):
    def render_to_response(self, context):
        return self.get_json_response(self.convert_context_to_json(context))

    def get_json_response(self, content, **httpresponse_kwargs):
        return http.HttpResponse(
            content,
            content_type='application/json',
            **httpresponse_kwargs
        )

    def convert_context_to_json(self, context):
        return json.dumps(context)


class ControlMixin(object):

    def update(self):

        self.sleep_mode = Config.objects.get(id="sleep_mode").value
        self.travel_mode = Config.objects.get(id="travel_mode").value

        global sunset_minus, sunset, sunrise, sunrise_plus, last_update
        now = datetime.datetime.now()
        if last_update + datetime.timedelta(days=1) < now:
            update_sun()

        if now > sunrise:
            self.night = sunset < now < sunrise_plus
        else:
            self.night = sunset_minus < now < sunrise

        self.bed_light = Device.objects.get(id="LT01")
        self.bed_motion_status = DeviceStatus.objects.get(
            device_id="MS01",
            codename="present",
        )
        self.bed_light_running_status = DeviceStatus.objects.get(
            device_id="LT01",
            codename="run",
        )
        self.living_light = Device.objects.get(id="LT02")
        self.living_motion_status = DeviceStatus.objects.get(
            device_id="MS02",
            codename="present",
        )
        self.living_light_running_status = DeviceStatus.objects.get(
            device_id="LT02",
            codename="run",
        )


class APIView(JSONResponseMixin, View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(APIView, self).dispatch(request, *args, **kwargs)


class DeviceView(APIView):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        device_id = kwargs["device_id"]
        try:
            device = Device.objects.get(pk=device_id)
            (result, message) = self.action(
                device=device,
                raw_data=request.body,
                data=request.POST,
                **kwargs
            )
        except Device.DoesNotExist:
            result = False
            message = "Device does not exist"

        context = {
            "response": result,
            "message": message,
        }
        return self.render_to_response(context)


#class DashboardView(LoginRequiredMixin, ListView):
class DashboardView(ControlMixin, TemplateView):
    template_name = 'control/dashboard.html'

    def get_context_data(self, **kwargs):
        global sunrise, sunset

        self.update()
        context = super(DashboardView, self).get_context_data(**kwargs)
        context['rooms'] = Room.objects.all()
        context['appliances'] = Device.objects.filter(type=control_constants.APPLIANCE)
        context['sunrise'] = sunrise
        context['sunset'] = sunset
        return context


class OperateView(DeviceView):

    def action(self, device, data, *args, **kwargs):
        return device.operate(kwargs["operation"], data)


class SwitchView(DeviceView):

    def action(self, device, data, *args, **kwargs):
        switch = kwargs["switch"]

        device.set_mode(switch)
        if switch == control_constants.MODE_ON:
            return device.operate("on", data)
        elif switch == control_constants.MODE_OFF:
            return device.operate("off", data)
        elif switch == control_constants.MODE_AUTO:
            return (True, "OK")
        else:
            return (False, "Unknown Switch Mode")


class OperationLogView(DeviceView):

    def action(self, device, raw_data, *args, **kwargs):
        return device.save_operation_log(int(kwargs["operation_log_id"]), raw_data)


class EventView(ControlMixin, DeviceView):

    def action(self, device, raw_data, *args, **kwargs):

        result = device.save_status_log(raw_data)
        self.update()

        if self.travel_mode != control_constants.True:
            if (
                    self.bed_light.get_mode() == control_constants.MODE_AUTO and
                    self.sleep_mode != control_constants.True and
                    self.night and
                    self.bed_motion_status.value == control_constants.ON and
                    self.bed_light_running_status.value == control_constants.OFF):
                self.bed_light.operate("on", {})

            if (
                    self.living_light.get_mode() == control_constants.MODE_AUTO and
                    self.night and
                    self.living_motion_status.value == control_constants.ON and
                    self.living_light_running_status.value == control_constants.OFF):
                self.living_light.operate("on", {})

        return result


class TimeView(ControlMixin, APIView):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):

        self.update()

        sleep_mode = Config.objects.get(id="sleep_mode")
        time = datetime.datetime.now().time()
        if time.hour == 9 and time.minute == 30:
            sleep_mode.value = control_constants.False
            sleep_mode.save()

        if self.travel_mode != control_constants.True:

            bed_motion_last_time = self.bed_motion_status.changed.astimezone(
                timezone.get_default_timezone()).replace(tzinfo=None)
            if (
                    self.bed_light.get_mode() == control_constants.MODE_AUTO and
                    bed_motion_last_time < datetime.datetime.now() - datetime.timedelta(minutes=10) and
                    self.bed_motion_status.value == control_constants.OFF and
                    self.bed_light_running_status.value == control_constants.ON):
                self.bed_light.operate("off", {})

            living_motion_last_time = self.living_motion_status.changed.astimezone(
                timezone.get_default_timezone()).replace(tzinfo=None)
            if (
                    self.living_light.get_mode() == control_constants.MODE_AUTO and
                    living_motion_last_time < datetime.datetime.now() - datetime.timedelta(minutes=10) and
                    self.living_motion_status.value == control_constants.OFF and
                    self.living_light_running_status.value == control_constants.ON):
                self.living_light.operate("off", {})

        result = True
        message = "OK"

        context = {
            "response": result,
            "message": message,
        }
        return self.render_to_response(context)


class ConfigView(ControlMixin, APIView):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):

        self.update()

        sleep_mode = Config.objects.get(id="sleep_mode")
        sleep_mode_value = request.POST.get("sleep_mode", None)
        if sleep_mode_value:
            sleep_mode.value = sleep_mode_value
            sleep_mode.save()

            if sleep_mode.value == control_constants.True:
                if self.bed_light_running_status.value == control_constants.ON:
                    self.bed_light.operate("off", {})

        result = True
        message = "OK"

        context = {
            "response": result,
            "message": message,
        }
        return self.render_to_response(context)
