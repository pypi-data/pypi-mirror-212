from typing import Any, Optional, Union
import urllib.request, urllib.parse, urllib.error
import json
import os
from uuid import getnode as get_mac
import qrcode
import io

VERSION = '0.1.6'

class Shellviz:
    def __init__(self, domain: Optional[str] = None, key: Optional[str] = None, id: Optional[str] = None, show_url: bool = True) -> None:
        """
        Initialize a new Shellviz instance
        
        Optional arguments:
        - domain: The domain of a self-hosted shellviz server. Defaults to https://shellviz.com
        - key: The API key for the shellviz server. Not required if using the free tier
        - id: The id of an existing instance to use. If not provided, a new instance will be created
        - show_url: Whether to print the instance url to the console on initialization. Defaults to True
        """
        self.domain = domain or os.environ.get('SHELLVIZ_DOMAIN', 'https://shellviz.com')
        self.key = key or os.environ.get('SHELLVIZ_API_KEY', '')
        self.instance_id = id or self._initalize_instance()

        if show_url and self.instance_id:
            print(self.get_url())


    def visualize(self, data: Any, id: str = None, fetch_url: bool = True) -> None:
        """
        Visualize the given data in Shellviz instance

        Required arguments:
        - data: The data to visualize. Can be a dict, list, or url

        Optional arguments:
        - id: The id to attach to the data. Defaults to None. If provided, any existing data with the same id will be replaced
        - fetch_url: Whether to attempt to download the data if it is a url. Defaults to True
        """
        if is_url(data):
            # if the user passed in a url, attempt to download the data
            data = download_url_data(data)

        url = '%s/api/visualize' % self.domain
        request_dict = self._generate_request_dict(data, self.instance_id, id)
        request_str = urllib.parse.urlencode(request_dict).encode('utf-8')
        try:
            req = urllib.request.urlopen(url, request_str)
        except urllib.error.HTTPError as e:
            return log_http_error(e)
        req.read()


    def get_url(self, show_qr_code=True, show_url=True) -> Optional[str]:
        """
        Returns the instance url. By default, prints the url to the console and displays a QR code

        Optional arguments:
        - show_qr_code: Whether to display a QR code for the instance url. Defaults to True
        - show_url: Whether to print the instance url to the console. Defaults to True
        """
        if not self.instance_id:
            return None

        instance_url = urllib.parse.urljoin(self.domain, self.instance_id)
        if show_qr_code:
            print(generate_qr(instance_url))
        if show_url:
            print(f'URL: {instance_url}')
        return instance_url
   

    @staticmethod
    def serialize(data):
        """
        Serializes the given data into a format that can be sent to the Shellviz server
        Mainly used to serialize Django models and querysets
        """
        data = serialize_django_data(data)
        return json.dumps(data)


    def _initalize_instance(self):
        """
        Initializes a new instance on the Shellviz server. Used internally by the constructor
        """
        url = '%s/api/channel' % self.domain
        request_dict = self._generate_request_dict()
        request_str = urllib.parse.urlencode(request_dict).encode('utf-8')
        try:
            req = urllib.request.urlopen(url, request_str)
        except urllib.error.HTTPError as e:
            return log_http_error(e)
        response = json.loads(req.read())
        return response['channel']
    

    def _generate_request_dict(self, data: Optional[dict] = None, instance_id: Optional[str] = None, id: Optional[str] = None):
        """
        Generates a request dict to send to the Shellviz server. Used internally by the visualize and _initalize_instance methods
        """
        request_dict = {
            'apiKey': self.key,
            'macAddress': get_mac() or '',
            'libraryLanguage': 'python',
            'libraryVersion': VERSION
        }
        if data:
            request_dict['data'] = Shellviz.serialize(data)
        if instance_id:
            request_dict['channel'] = instance_id
        if id:
            request_dict['id'] = id
        return request_dict


# Helper Utils
def log_http_error(e):
    """
    Logs an error from an HTTP request to the console
    """
    print('The server couldn\'t fulfill the request.')
    print('URL: ', e.url)
    print('Error code: ', e.code)
    print('Error message: ', e.read())


def generate_qr(url: str) -> str:
    """
    Generates a QR code for the given url
    """
    qr = qrcode.QRCode()
    qr.add_data(url)
    qr.make(fit=True)

    f = io.StringIO()
    qr.print_ascii()
    f.seek(0)
    return f.read()

def is_url(data: Any) -> bool:
    """
    Returns True if the given string is a url
    """
    return isinstance(data, str) and bool(urllib.parse.urlparse(data).scheme and urllib.parse.urlparse(data).netloc)


def download_url_data(url: str) -> Union[str, dict]:
    """
    Attempts to download the data from the given url
    """
    try:
        req = urllib.request.urlopen(url)
    except urllib.error.HTTPError as e:
        return log_http_error(e)

    result = req.read()
    
    # try to parse as json
    try:
        result = json.loads(result)
    except:
        pass

    return result


def serialize_django_data(data):
    """
    Checks if the given data is a Django model or queryset and serializes it
    If the data is not a Django model or queryset, returns the data unchanged
    If Django is not installed, returns the data unchanged
    """
    try:
        from django.db.models import QuerySet
        from django.db.models import Model
        from django.core import serializers
    except ImportError:
        django_enabled = False
    else:
        django_enabled = True

    if django_enabled:
        if isinstance(data, Model):
            data = [data]
        elif isinstance(data, QuerySet):
            data = list(data)
        if isinstance(data, list) and len(data) and isinstance(data[0], Model):
            data = json.loads(serializers.serialize('json', data))
            data = [serialized_model['fields'] for serialized_model in data]
    return data