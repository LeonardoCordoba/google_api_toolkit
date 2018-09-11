class Query:

    def __init__(self):

        self.priority = 'INTERACTIVE'
        self.allowLargeResults = False
        self.useLegacySql = False
        self.jobData = None
        self.query = None
        self.job_type = None
        self.writeDisposition = 'WRITE_EMPTY'
        self.createDisposition = "CREATE_IF_NEEDED"
        self.datasetId = None
        self.tableId = None
        self.dml = False

    def query_config(self, large_results=False, legacy_sql=False, priority='INTERACTIVE',
                     write_disposition= 'WRITE_EMPTY', dataset_id = None, table_id = None,
                     create_disposition = "CREATE_IF_NEEDED", ):
        self.priority = priority
        self.allowLargeResults = large_results
        self.useLegacySql = legacy_sql
        self.writeDisposition = write_disposition
        self.datasetId = dataset_id
        self.tableId = table_id
        self.createDisposition = create_disposition


    def set_query(self, query, populate_table=False, dml = False):
        self.dml = dml
        #TODO hacer metodo que arme la configuracion de la query a partir de un .cfg
        self.query = query

        if not populate_table:

            self.job_type = "not_populate"
            self.jobData = {
                'configuration': {
                    'query': {
                        'query': query,
                        'priority': self.priority,
                        'allowLargeResults': self.allowLargeResults,
                        'useLegacySql': self.useLegacySql,
                        'writeDisposition' : self.writeDisposition,
                        'createDisposition' : self.createDisposition
                    }
                }
            }
        else:
            self.job_type = "populate"
            self.jobData = {
                'configuration': {
                    'query': {
                        'query': self.query,
                        'priority': self.priority,
                        'allowLargeResults': self.allowLargeResults,
                        'useLegacySql': self.useLegacySql,
                        'writeDisposition': self.writeDisposition,
                        'createDisposition': self.createDisposition,
                        "destinationTable": {
#                            'projectId': self.BigQueryConnection.projectId,   TODO: este param lo tiene connection, probar si anda sin esto
                            'datasetId': self.datasetId,
                            'tableId': self.tableId
                        }
                    }
                }
            }

        if self.dml == True:
            self.jobData["configuration"]["query"].pop("createDisposition")
            self.jobData["configuration"]["query"].pop("writeDisposition")