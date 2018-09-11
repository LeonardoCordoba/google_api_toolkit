class Table:

    def __init__(self):

        self.tableId = None
        self.datasetId = None
        self.jobData = None
        self.job_type = None

    def table_config(self, table_id, dataset_id):
        self.tableId = table_id
        self.datasetId = dataset_id

    def export_to_bucket(self, destination_bucket, destination_object, destination_format, field_delimiter = "|"):
        # TODO: se puede agregar compression = "GZIP"
        self.job_type = "export"
        destinationUris = "gs://" + destination_bucket + "/" + destination_object

        self.jobData = {
            'configuration': {
                'extract': {
                    'sourceTable': {
#                        'projectId': projectId, TODO: este parametro lo tiene connection, ver si anda sin esto, en todo caso el job tendria q modificarlo
                        'datasetId': self.datasetId,
                        'tableId': self.tableId
                    },
                    'destinationUris': [destinationUris],
                    'destinationFormat': destination_format,
                    'fieldDelimiter': field_delimiter
                }
            }
        }

    def delete_table(self):
        self.job_type = "delete"
