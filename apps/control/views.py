
import json

from django import http
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import (
    View,
    TemplateView,
)

#from apps.auth.views import LoginRequiredMixin

import apps.control as control_constants
from apps.control.models import (
    Device,
    DeviceOperation,
)


class APIView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(APIView, self).dispatch(request, *args, **kwargs)


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


#class DashboardView(LoginRequiredMixin, ListView):
class DashboardView(TemplateView):
    template_name = 'control/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        context['data'] = 'hello world'
        return context


class TriggerView(JSONResponseMixin, APIView):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        deviceID = request.GET.get("device", "")
        operation_codename = request.GET.get("operation", "")
        try:
            device = Device.objects.get(pk=deviceID)
            operation = DeviceOperation.objects.get(
                device=device,
                codename=operation_codename,
            )
            (result, message) = self.trigger(
                device=device,
                operation=operation,
                event_id=kwargs.get("event_id", 0),
                params=request.body,
            )
        except Device.DoesNotExist:
            result = False
            message = "Device does not exist"
        except DeviceOperation.DoesNotExist:
            result = False
            message = "Device operation does not exist"

        context = {
            "response": result,
            "message": message,
        }
        return self.render_to_response(context)


class OperateView(TriggerView):

    def trigger(self, *args, **kwargs):
        device = kwargs["device"]
        operation = kwargs["operation"]
        print kwargs
        return device.operate(operation)


class EventView(TriggerView):

    def trigger(self, *args, **kwargs):
        device = kwargs["device"]
        operation = kwargs["operation"]
        event_id = int(kwargs["event_id"])
        params = kwargs["params"]

        if event_id == control_constants.EVENT_TIME:
            print "time"
            return (True, "")
        elif event_id == control_constants.EVENT_TRIGGER:
            return device.save_log(operation, control_constants.REMOTE, params)
        else:
            return (False, "Unknow event")
