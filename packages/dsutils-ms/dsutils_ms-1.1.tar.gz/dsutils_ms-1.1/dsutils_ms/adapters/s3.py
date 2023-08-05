from dsutils_ms.adapters.interface import ConnectorAdapterInterface

from typing import Any, Dict

from pyspark.sql import DataFrame


class S3(ConnectorAdapterInterface):
    """`` S3`` upload and download files from S3.
    Example:
    ::
        >>>  S3(S3_access = <aws_region:access_key:secret_key:bucket>)
    """

    def __init__(self, spark, S3_bucket):
        """Creates a new instance of  S3

        Args:
            spark: Spark session.
            S3_bucket: S3 Bucket.
        """

        self._spark = spark
        self._root = f"s3a://{S3_bucket}/"
        self._path = None

    def load(self, filename, data, mode="overwrite", header=True) -> bool:
        """Upload a file to S3.

        Returns:
            Boolean whether the file was uploaded or not.
        """
        try:
            extension = filename.split(".")[-1]
            self._path = self._root + filename

            if extension == "csv":
                data.write.csv(self._path, mode=mode, header=header)
            elif extension == "json":
                data.write.json(self._path, mode=mode)
            elif extension == "parquet":
                data.write.parquet(self._path, mode=mode)
            else:
                raise Exception("File extension not supported.")
            return True
        except Exception as e:
            raise Exception("Error uploading file to S3.") from e
            return False

    def upload(self, filename, data) -> bool:
        """Upload a file to S3.

        Returns:
            Boolean whether the file was uploaded or not.
        """

        return self.load(filename, data)

    def save(self, filename, inferSchema=True, header=True) -> DataFrame:
        """Download a file from S3.

        Returns:
            PySpark DataFrame.
        """

        try:
            extension = filename.split(".")[-1]
            self._path = self._root + filename

            if extension == "csv":
                data = self._spark.read.csv(
                    self._path, inferSchema=inferSchema, header=header
                )
            elif extension == "json":
                data = self._spark.read.json(self._path)
            elif extension == "parquet":
                data = self._spark.read.parquet(
                    self._path, inferSchema=inferSchema, header=header
                )
            else:
                raise Exception("File extension not supported.")
            return data
        except Exception as e:
            raise Exception("Error downloading file from S3.") from e
            return None

    def download(self, filename) -> DataFrame:
        """Download a file from S3.

        Returns:
            PySpark DataFrame.
        """

        return self.save(filename)

    def read(self, filename) -> DataFrame:
        """Download a file from S3.

        Returns:
            PySpark DataFrame.
        """

        return self.save(filename)

    def describe(self) -> Dict[str, Any]:
        """Returns a dict that describes the attributes of the connection.

        Returns:
            Dictionary with all parameters.
        """

        return dict(root=self._root, path=self._path)
