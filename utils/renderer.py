from rest_framework.renderers import JSONRenderer
from rest_framework.utils import json
from utils.response import create_template

class JSONResponseRenderer(JSONRenderer):
    media_type = 'application/json'
    charset = 'utf-8'

    def render(self, data, status=200, accepted_media_type=None, renderer_context=None):
        message = data.get('message', '')
        error = data.get('error', False)
        return json.dumps(
            create_template(
                context=data.get("data"), 
                status=False if error else True,
                message=message
            )
        )