import requests
import json
import os
from dataclasses import dataclass, asdict
from typing import List

API_BASE_URL = """https://the-one-api.dev/v2"""
API_KEY = os.environ.get("LOTR_API_KEY")
if not API_KEY:
    API_KEY = os.getenv("LOTR_API_KEY")
if not API_KEY:
    raise AssertionError("Please set the environment variable 'LOTR_API_KEY'")

@dataclass
class BaseResponse:
    docs: List = None
    limit: int = None
    offset: int = None
    page: int = None
    pages: int = None
    total: int = None
    error: str = None


@dataclass
class ApiError:
    code: int
    msg: str


class BaseRequestHandler:
    # to be defined by subclasses
    class_type = None
    class_type_all = None
    url_base = ""

    def _call(self, url, headers=None, params=None):
        return requests.get(url, headers=headers, params=params)

    def _get(self, url, params=None):
        headers = {'Authorization': f"Bearer {API_KEY}"}
        response = self._call(f"{API_BASE_URL}/{url}", headers=headers, params=params)
        if 200 <= response.status_code < 300:
            response_json = json.loads(response.text)
            print(response_json)
        else:
            response_json = json.loads(response.text)

            response_json = {'error': asdict(ApiError(code=response.status_code, msg=f"""An error was returned from the API: {response_json['message']}"""))}

        return response_json

    def _get_one(self, url):
        response = self._get(url)
        try:
            match = response.get("docs")[0]
            result = self.class_type(**match)
        except (TypeError, IndexError):
            if response.get("error"):
                return response.get("error")
            else:
                return self.class_type({"error": "No match"})
        return result

    def _get_all(self, url, **kwargs):
        q_params = kwargs
        filter_str = q_params['filter_string']
        del q_params['filter_string']
        if filter_str:
            filter_key = filter_str.split("=")[0]
            filter_val = filter_str.split("=")[1]
            q_params[filter_key] = filter_val

        response = self._get(url, params=q_params)

        response_list = []
        for d in response.get('docs', []):
            response_list.append(self.class_type(**d))
        response['docs'] = response_list
        result = self.class_type_all(**response)

        return result
