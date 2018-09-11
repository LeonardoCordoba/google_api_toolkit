from google_api_toolkit.base import job
from google_api_toolkit.big_query import connection as c
from google_api_toolkit.big_query import query as q
from google_api_toolkit.big_query import table as t
import sys
import time


class Job(job.Job):

    def __init__(self, connection_object, request_object):
        super(Job, self).__init__()
        if not isinstance(connection_object, c.Connection):
            raise Exception('connection_object parameter must be of type google_analytics.connection.Connection')
        else:
            self.connection = connection_object

        if not isinstance(request_object, q.Query) and not isinstance(request_object, t.Table):
            raise Exception('request_object parameter must be of type big_query.Query')
        else:
            self.request = request_object

        if self.request.job_type == "populate":
            self.request.jobData['configuration']['query']['destinationTable']['projectId'] = self.connection.projectId


    def execute(self):
        """
        This method executes a query, delete or export
        :return:
        None
        """
        if self.request.job_type == "delete":
            print(self.request.job_type)
            add = self.connection.service.tables().\
                delete(projectId = self.connection.projectId, datasetId = self.request.datasetId,
                       tableId = self.request.tableId).execute()
            print('Result add: %s' % str(add))

        elif (self.request.job_type == "populate") | (self.request.job_type == "not_populate") | (self.request.job_type == "export"):
            jobCollection = self.connection.service.jobs()
            insertResponse = jobCollection.insert(projectId = self.connection.projectId, body=self.request.jobData).execute(http=self.connection.http)

            while True:

                status = jobCollection.get(projectId=self.connection.projectId, jobId=insertResponse['jobReference']['jobId']).execute(http=self.connection.http)
                currentStatus = status['status']['state']
                if 'DONE' == currentStatus:
                    print('Current status: ' + currentStatus)
                    print(time.ctime())
                    if status['status'].get('errors'):
                        print('Error: %s' % str(status['status']['errors'][0]['message']))
                        sys.exit(1)
                    return insertResponse

                else:
                    print('Waiting for the job to complete...')
                    print('Current status: ' + currentStatus)
                    print(time.ctime())
                    time.sleep(4)




