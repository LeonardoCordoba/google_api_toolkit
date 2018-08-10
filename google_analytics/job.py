from google_api_toolkit.base import job
from google_api_toolkit.google_analytics import connection as c
from google_api_toolkit.google_analytics import report as r
from google_api_toolkit.google_analytics import response as res


class Job(job.Job):

    def __init__(self, connection_object, request_object):
        super(Job, self).__init__()
        if not isinstance(connection_object, c.Connection):
            raise Exception('connection_object parameter must be of type google_analytics.connection.Connection')
        else:
            self.connection = connection_object

        if not isinstance(request_object, r.Report):
            raise Exception('request_object parameter must be of type base.request.Request')
        else:
            self.request = request_object

    def execute(self, results_offset=None):
        request_body = self.request.request_body
        api_response = self.connection.service.reports().batchGet(body=request_body).execute()
        self.response = res.Response(api_response, self.request.page_size)
        return self.response
        #self.response = response.Response(api_response, self.request.report.page_size)


    # ------------------------------- TODO: VER QUÉ HACE, VIENE DE google_analytics.query
'''    
def get_all_pages(self):
        assert self.__request is not None, 'Query object required a request object to be set.'

        self.execute()
        self.__response_pages.append(self.__response)

        self.__total_results = self.__response.total_rows
        self.__total_pages = math.ceil(self.total_results / self.__request.report.page_size)

        self.__sampling_rate = self.__response.sampling_rate

        while(self.current_page < self.total_pages):
            self.__current_page += 1
            self.request.report.next_page = self.__current_page
            self.execute()
            self.__response_pages.append(self.__response)

'''

