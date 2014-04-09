
import json
import datetime

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


class APIView(JSONResponseMixin, View):
    http_method_names = ['post']

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(APIView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        device_id = kwargs["device_id"]
        print request.body
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
class DashboardView(TemplateView):
    template_name = 'control/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        context['rooms'] = Room.objects.all()
        context['appliances'] = Device.objects.filter(type=control_constants.APPLIANCE)
        return context


class OperateView(APIView):

    def action(self, device, data, *args, **kwargs):
        return device.operate(kwargs["operation"], data)


class OperationLogView(APIView):

    def action(self, device, raw_data, *args, **kwargs):
        return device.save_operation_log(int(kwargs["operation_log_id"]), raw_data)


class EventView(APIView):

    def action(self, device, raw_data, *args, **kwargs):

        result = device.save_status_log(raw_data)

        sleep_mode = Config.objects.get(id="sleep_mode").value
        night = True

        bed_light = Device.objects.get(id="LT01")
        bed_motion_status = DeviceStatus.objects.get(
            device_id="MS01",
            codename="present",
        )
        bed_light_running_status = DeviceStatus.objects.get(
            device_id="LT01",
            codename="run",
        )
        living_light = Device.objects.get(id="LT02")
        living_motion_status = DeviceStatus.objects.get(
            device_id="MS02",
            codename="present",
        )
        living_light_running_status = DeviceStatus.objects.get(
            device_id="LT02",
            codename="run",
        )

        if sleep_mode != control_constants.True and night:
            if bed_motion_status.value == control_constants.ON and \
                    bed_light_running_status.value == control_constants.OFF:
                bed_light.operate("on", {})

        if night:
            if living_motion_status.value == control_constants.ON and \
                    living_light_running_status.value == control_constants.OFF:
                living_light.operate("on", {})

        return result


class TimeView(JSONResponseMixin, View):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        bed_light = Device.objects.get(id="LT01")
        bed_motion_status = DeviceStatus.objects.get(
            device_id="MS01",
            codename="present",
        )
        bed_light_running_status = DeviceStatus.objects.get(
            device_id="LT01",
            codename="run",
        )
        living_light = Device.objects.get(id="LT02")
        living_motion_status = DeviceStatus.objects.get(
            device_id="MS02",
            codename="present",
        )
        living_light_running_status = DeviceStatus.objects.get(
            device_id="LT02",
            codename="run",
        )

        bed_motion_last_time = bed_motion_status.changed.astimezone(timezone.get_default_timezone()).replace(tzinfo=None)
        if bed_motion_last_time < datetime.datetime.now() - datetime.timedelta(minutes=10):
            if bed_motion_status.value == control_constants.OFF and \
                    bed_light_running_status.value == control_constants.ON:
                bed_light.operate("off", {})

        living_motion_last_time = living_motion_status.changed.astimezone(timezone.get_default_timezone()).replace(tzinfo=None)
        if living_motion_last_time < datetime.datetime.now() - datetime.timedelta(minutes=10):
            if living_motion_status.value == control_constants.OFF and \
                    living_light_running_status.value == control_constants.ON:
                living_light.operate("off", {})

        result = True
        message = "OK"

        context = {
            "response": result,
            "message": message,
        }
        return self.render_to_response(context)
