
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
                data=request.body,
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
        context['data'] = 'hello world'
        return context


class OperateView(APIView):

    def action(self, device, data, *args, **kwargs):
        return device.operate(kwargs["operation"])


class OperationLogView(APIView):

    def action(self, device, data, *args, **kwargs):
        return device.save_operation_log(int(kwargs["operation_log_id"]), data)


class EventView(APIView):

    def action(self, device, data, *args, **kwargs):
        event_id = int(kwargs["event_id"])

        if event_id == control_constants.EVENT_TIME:
            print "time"
            return (True, "OK")
        elif event_id == control_constants.EVENT_TRIGGER:
            return device.save_status_log(data)
        else:
            return (False, "Unknow event")
