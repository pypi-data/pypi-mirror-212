from dsutils_ms.adapters.interface import ConnectorAdapterInterface

from typing import Any, Dict
import boto3
import time


class DynamoDB(ConnectorAdapterInterface):
    """``DynamoDB`` execute select and update statements in DynamoDB databases.

    Example:
    ::
        >>> DynamoDB(uri = <DynamoDB_uri>)
    """

    def __init__(self, aws_region, access_key, secret_key, table_name):
        """Creates a new instance of DynamoDB

        Args:
            aws_region: AWS Region
            access_key: AWS Access Key
            secret_key: AWS Secret Key
            table: DynamoDB Table
        """
        self._aws_region = aws_region
        self._access_key = access_key
        self._secret_key = secret_key
        self._table_name = table_name

        try:
            self._client = boto3.resource(
                "dynamodb",
                region_name=self._aws_region,
                aws_access_key_id=self._access_key,
                aws_secret_access_key=self._secret_key,
            )
            self._table = self._client.Table(self._table_name)
        except Exception as e:
            raise Exception("DynamoDB Connection Error") from e

    def load(self) -> None:
        """Run select statement on DynamoDB.

        Returns:
            None
        """
        raise NotImplementedError

    def save(self, data, wait=0.25) -> bool:
        """Run insert statement on DynamoDB.

        Returns:
            True if success, False otherwise.
        """
        try:
            with self._table.batch_writer() as batch:
                for item in data:
                    batch.put_item(Item=item)
                    time.sleep(wait)

            return True
        except Exception as e:
            raise Exception("Save Table Error") from e
            return False

    def describe(self) -> Dict[str, Any]:
        """Returns a dict that describes the attributes of the connection.

        Returns:
            Dictionary with all parameters.
        """

        return dict(
            aws_region=self._aws_region,
            access_key=self._access_key,
            secret_key=self._secret_key,
            table_name=self._table_name,
        )
