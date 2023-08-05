from dsutils_ms.adapters.interface import ConnectorAdapterInterface

from typing import Any, Dict
from pyspark.sql import DataFrame


class MySQL(ConnectorAdapterInterface):
    """``MySQL`` execute select and update statements in MySQL databases.

    Example:
    ::
        >>> MySQL(uri = <mysql_uri>)
    """

    def __init__(self, spark, jdbc_url, jdbc_user, jdbc_pass):
        """Creates a new instance of MySQL

        Args:
            mysql_uri: Database URL.
        """
        self._spark = spark
        self._jdbc_url = jdbc_url
        self._jdbc_user = jdbc_user
        self._jdbc_pass = jdbc_pass

        try:
            self._spark.read.format("jdbc").option(
                "url", self._jdbc_url
            ).option("user", self._jdbc_user).option(
                "password", self._jdbc_pass
            ).option(
                "query", "SELECT 1 AS dummy"
            ).load()
        except Exception as e:
            raise Exception("Spark JDBC Configuration Error") from e

    def create(self, table, df) -> bool:
        """Run create statement on MySQL.

        Returns:
            True / False.
        """

        try:
            self.insert(table, df, overwrite=True)
            return True
        except Exception as e:
            raise Exception("Create Table Error") from e
            return False

    def select(self, query) -> DataFrame:
        """Run select statement on MySQL.

        Returns:
            PySpark DataFrame.
        """
        return self.load(query)

    def load(self, query) -> DataFrame:
        """Run select statement on MySQL.

        Returns:
            PySpark DataFrame.
        """

        self._query = query.replace("\n", " ")

        try:
            df = (
                self._spark.read.format("jdbc")
                .option("url", self._jdbc_url)
                .option("user", self._jdbc_user)
                .option("password", self._jdbc_pass)
                .option("query", query)
                .load()
            )

            df_sql = self._spark.createDataFrame(df.collect())

            return df_sql
        except Exception as e:
            raise Exception("Load Table Error") from e
            return None

    def insert(self, table, df, overwrite=False) -> DataFrame:
        """Run insert statement on MySQL.

        Returns:
            PySpark DataFrame.
        """
        return self.save(table, df, overwrite)

    def save(self, table, df, overwrite=False) -> bool:
        """Run insert statement on MySQL.

        Returns:
            PySpark DataFrame.
        """
        try:
            if overwrite:
                spark_mode = "overwrite"
            else:
                spark_mode = "append"

            df.write.format("jdbc").option("url", self._jdbc_url).option(
                "user", self._jdbc_user
            ).option("password", self._jdbc_pass).option(
                "dbtable", table
            ).mode(
                spark_mode
            ).save()

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
            jdbc_url=self._jdbc_url,
            jdbc_user=self._jdbc_user,
            jdbc_pass=self._jdbc_pass,
        )
