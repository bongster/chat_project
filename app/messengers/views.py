from django.shortcuts import render

from django.views.generic import TemplateView, View

from app.utils import JSONResponseMixin

# Create your views here.

class MessengersView(TemplateView):
    template_name = './index.html'

class RoomsView(JSONResponseMixin, TemplateView):

    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, **response_kwargs)
