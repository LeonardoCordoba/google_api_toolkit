from google_api_toolkit.base import connection as c

from oauth2client.service_account import ServiceAccountCredentials
import httplib2
from apiclient.discovery import build


class Connection(c.Connection):

    def __init__(self):
        self.service = None
        self.report = []

        self.scope = ['https://www.googleapis.com/auth/analytics.readonly']
        self.discovery_uri = 'https://analyticsreporting.googleapis.com/$discovery/rest'
        self.api_name = 'analyticsreporting'
        self.api_version = 'v4'

        self.sampling_rate = 1
        self.next_page_token = None
        self.total_results = 0
        self.total_pages = 1
        self.current_page = 1
        self.response_pages = []

    def config_service(self, key_file_path):
        self.key_file_path = key_file_path
        credentials = ServiceAccountCredentials.from_json_keyfile_name(self.key_file_path, self.scope)
        self.http = credentials.authorize(httplib2.Http())
        self.service = build(serviceName=self.api_name, http=self.http, version=self.api_version,
                                 discoveryServiceUrl=self.discovery_uri)



