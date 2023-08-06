import json
import requests
from NikGapps.helper.Statics import Statics


class Requests:

    @staticmethod
    def get(url, headers=None, params=None):
        if params is None:
            params = {"": ""}
        if headers is None:
            headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:105.0) Gecko/20100101 Firefox/105.0'}
        return requests.get(url, data=json.dumps(params), headers=headers)

    @staticmethod
    def put(url, headers=None, params=None):
        if params is None:
            params = {"": ""}
        if headers is None:
            headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:105.0) Gecko/20100101 Firefox/105.0'}
        return requests.put(url, data=json.dumps(params), headers=headers)

    @staticmethod
    def patch(url, headers=None, params=None):
        if params is None:
            params = {"": ""}
        if headers is None:
            headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:105.0) Gecko/20100101 Firefox/105.0'}
        return requests.patch(url, data=json.dumps(params), headers=headers)

    @staticmethod
    def post(url, headers=None, params=None):
        if params is None:
            params = {"": ""}
        if headers is None:
            headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:105.0) Gecko/20100101 Firefox/105.0'}
        return requests.post(url, data=json.dumps(params), headers=headers)

    @staticmethod
    def get_text(url):
        return requests.get(url).text

    @staticmethod
    def get_release_date(android_version, release_type):
        decoded_hand = Requests.get("https://raw.githubusercontent.com/nikgapps/tracker/main/count.json")
        if decoded_hand.status_code == 200:
            data = decoded_hand.json()
            if android_version in data[release_type]:
                return data[release_type][android_version]
        else:
            print(decoded_hand.status_code)
            return Statics.time
