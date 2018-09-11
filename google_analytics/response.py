from google_api_toolkit.base import response as r
import itertools
import pandas as pd
import math


# TODO: validate when response is an error or has no body
class Response(r.Response):
    def __init__(self, api_response, rows_per_page):
        super().__init__()
        self.api_response = api_response
        self.rows_per_page = rows_per_page
        self.total_rows = 0
        self.sampling_rate = None
        self.parse_body()

    # ------------------------------------------------------------------------
    def parse_body(self):
        report = self.api_response.get('reports', [])[0]
        report_data = report.get('data', {})

        self.total_rows = report_data.get('rowCount')
        self.total_pages = math.ceil(report_data.get('rowCount') / self.rows_per_page)


        if 'samplingSpaceSizes' in report_data.keys():
            self.sampling_rate = int(report_data.get('samplesReadCounts')[0]) / int(report_data.get('samplingSpaceSizes')[0])

        columnHeader = report.get('columnHeader', {})
        dimensionHeaders = columnHeader.get('dimensions', [])
        metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])

        columns = list(map(lambda x: x.replace('ga:', ''), dimensionHeaders))
        columns.extend(map(lambda x: x['name'].replace('ga:', ''), metricHeaders))
        data = list(map(lambda row: list(itertools.chain(row['dimensions'], row['metrics'][0]['values'])),
                        report_data.get('rows', [])))

        df = pd.DataFrame(data, columns=columns)

        self.response_body = df
