from google_api_toolkit.base import connection as c
from googleapiclient.discovery import build, DISCOVERY_URI
from oauth2client.service_account import ServiceAccountCredentials
from oauth2client.client import AccessTokenRefreshError
import httplib2


class Connection(c.Connection):

    def __init__(self):
        self.projectId = None
        self.service = None
        self.scope = 'https://www.googleapis.com/auth/bigquery'
        self.http = None
        self.discovery_uri = DISCOVERY_URI

    def set_scope(self, readonly = False):
        if readonly:
            self.scope = 'https://www.googleapis.com/auth/bigquery.readonly'
        else:
            self.scope = 'https://www.googleapis.com/auth/bigquery'

    def set_project_id(self,project_id):
        self.projectId = project_id

    def config_service(self, key_file):
        try:
            self.key_file_path = key_file
            credentials = ServiceAccountCredentials.from_json_keyfile_name(self.key_file_path, self.scope)
            self.http = credentials.authorize(httplib2.Http())
            self.service = build(serviceName="bigquery", http=self.http, version="v2",
                                 discoveryServiceUrl=self.discovery_uri)

        except AccessTokenRefreshError:
            print ("Credentials have been revoked or expired, please re-run the application to re-authorize")
            sys.exit(1)

