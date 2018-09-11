from google_api_toolkit.base import job
from google_api_toolkit.google_analytics import connection as c
from google_api_toolkit.google_analytics import report as r
from google_api_toolkit.google_analytics import response as res
import pandas as pd

class Job(job.Job):

    def __init__(self, connection_object, request_object):
        super(Job, self).__init__()
        self.api_response = None
        if not isinstance(connection_object, c.Connection):
            raise Exception('connection_object parameter must be of type google_analytics.connection.Connection')
        else:
            self.connection = connection_object

        if not isinstance(request_object, r.Report):
            raise Exception('request_object parameter must be of type base.request.Request')
        else:
            self.request = request_object

    def execute(self):
        request_body = self.request.request_body
        self.api_response = self.connection.service.reports().batchGet(body=request_body).execute()
        acumulated_response = res.Response(self.api_response, self.request.page_size)
        print("acum:",acumulated_response.total_rows)
        print("page_token inicial:", float(self.request.page_token))
        while float(self.request.page_token) + self.request.page_size < acumulated_response.total_rows:
            self.request.page_token = self.api_response["reports"][0]["nextPageToken"]
            self.request.build_report_body()
            request_body = self.request.request_body
            self.api_response = self.connection.service.reports().batchGet(body=request_body).execute()
            new_response = res.Response(self.api_response, self.request.page_size)
            acumulated_response.response_body = pd.concat([acumulated_response.response_body, new_response.response_body])
        self.response = acumulated_response
        return self.response
