from google_api_toolkit.google_analytics import utils


class Report():

    def __init__(self):
        self.view_id = None
        self.date_ranges = []
        self.metrics = []
        self.dimensions = []
        self.filters = []

        self.next_page = None

        self.sampling_level = 'LARGE'
        self.page_size = 10000

        self.request_body = None

    # ------------------------------------------------------------------------
    def set_view_id(self, view_id):
        self.view_id = view_id

    # ------------------------------------------------------------------------
#    @property
#    def page_size(self):
#        return self.page_size


    # ------------------------------------------------------------------------
#    @property
#    def next_page(self):
#        return self.next_page


    # ------------------------------------------------------------------------
#    @next_page.setter
#    def next_page(self, value):
#        self.next_page = value


    # ------------------------------------------------------------------------
    # TODO: validate input
    def add_date_range(self, start_date, end_date):
        assert utils.validate_date_range(start_date, end_date)
        self.date_ranges.append((start_date, end_date))

    # ------------------------------------------------------------------------
    # TODO: validate input
    def add_metric(self, name):
        self.metrics.append(name)


    # ------------------------------------------------------------------------
    # TODO: validate input
    def add_dimension(self, name):
        self.dimensions.append(name)


    # ------------------------------------------------------------------------
    def add_filter(self, dimension, operator, expression, negate=False):
        self.filters.append((dimension, operator, expression, negate))


    # ------------------------------------------------------------------------
    # TODOL nextPageToken not showing up
    def build_report_body(self):
        self.request_body = {'reportRequests': [{
            'viewId': str(self.view_id),
            'dateRanges': [{'startDate': range[0], 'endDate': range[1]} for range in self.date_ranges],
            'metrics': [{'expression': metric} for metric in self.metrics],
            'dimensions': [{'name': dimension} for dimension in self.dimensions],
            'dimensionFilterClauses': [{
                'filters': [{'dimensionName': filter[0], 'operator': filter[1], 'expressions': filter[2], 'not': str(filter[3]).lower()}
                            for filter in self.filters]
            }],
            'samplingLevel': self.sampling_level,
            'pageSize': self.page_size
        }
        ]
        }

 #       if self.next_page is not None:
 #           self.request_body['pageToken'] = str(self.next_page * self.page_size)