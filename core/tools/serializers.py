from rest_framework.parsers import DataAndFiles, FormParser, JSONParser, MultiPartParser
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer

from core.helpers.convert_keys import convert_keys


class JSONCamelRenderer(JSONRenderer):
    media_type = "application/json"
    format = "json"

    def render(self, data, *args, **kwargs):
        data = convert_keys(data, to_case="camelcase")
        return super(JSONCamelRenderer, self).render(data, *args, **kwargs)


class BrowsableAPICamelRenderer(BrowsableAPIRenderer):
    def render(self, data, *args, **kwargs):
        data = convert_keys(data, to_case="camelcase")
        return super(BrowsableAPICamelRenderer, self).render(data, *args, **kwargs)


class JSONCamelParser(JSONParser):
    media_type = "application/json"
    renderer_class = JSONCamelRenderer

    def parse(self, *args, **kwargs):
        data = super(JSONCamelParser, self).parse(*args, **kwargs)
        return convert_keys(data, to_case="snakecase", show_none=True)


class FormCamelParser(FormParser):
    def parse(self, *args, **kwargs):
        data = super(FormCamelParser, self).parse(*args, **kwargs)
        return convert_keys(data, to_case="snakecase", show_none=True)


class MultiPartCamelParser(MultiPartParser):
    def parse(self, *args, **kwargs):
        data_files: DataAndFiles = super(MultiPartCamelParser, self).parse(
            *args, **kwargs
        )
        data_files.data = convert_keys(
            data_files.data,
            to_case="snakecase",
            show_none=True,
        )
        return data_files
