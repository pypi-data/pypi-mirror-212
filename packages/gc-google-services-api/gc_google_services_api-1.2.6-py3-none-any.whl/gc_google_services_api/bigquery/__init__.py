import logging
from google.cloud import bigquery
from google.api_core.exceptions import NotFound

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def execute_query(query="", error_value=[]):
    """
    DEPRECATED: Now use BigQueryManager class instead this method.
    """
    client = bigquery.Client()
    query_job = client.query(query)

    try:
        return query_job.result()
    except Exception as e:
        print('[ERROR]: ', e)
        return error_value


class BigQueryManager:
    def __init__(self, project_id, dataset_id):
        self.project_id = project_id
        self.dataset_id = dataset_id

        self.client = bigquery.Client(project=project_id)

    def create_table_if_not_exists(self, table_id, schema={}):
        def _parse_schemas():
            schema_fields = []
            for field_name, field_type in schema.items():
                schema_fields.append(
                    bigquery.SchemaField(field_name, field_type))

            return schema_fields

        try:
            self.client.get_table(
                f"{self.project_id}.{self.dataset_id}.{table_id}"
            )
        except NotFound:
            table_ref = self.client.dataset(self.dataset_id).table(table_id)
            table = bigquery.Table(table_ref, schema=_parse_schemas())
            self.client.create_table(table)

    def execute_query(self, query="", error_value=[]):
        query_job = self.client.query(query)

        try:
            return query_job.result()
        except Exception as e:
            logging.info(query)
            logging.error(f"[ERROR - execute_query]: {e}")
            return error_value
