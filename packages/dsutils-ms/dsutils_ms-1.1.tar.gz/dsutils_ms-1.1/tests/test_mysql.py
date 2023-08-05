from unittest import TestCase

from dsutils_ms.adapters.mysql import MySQL
from dsutils_ms.helpers.env import get_credential

from fixtures.spark import spark
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    IntegerType,
    TimestampType,
)


class TestMySQL(TestCase):
    def test_mysql_describe(self):
        jdbc_url = get_credential("ANALYTICS_DB_JDBC")
        jdbc_user = get_credential("ANALYTICS_DB_USER")
        jdbc_pass = get_credential("ANALYTICS_DB_PASS")

        db_analytics = MySQL(
            spark=spark(),
            jdbc_url=jdbc_url,
            jdbc_user=jdbc_user,
            jdbc_pass=jdbc_pass,
        ).describe()

        self.assertEqual(isinstance(db_analytics, dict), True)

    def test_mysql_create(self):
        jdbc_url = get_credential("ANALYTICS_DB_JDBC")
        jdbc_user = get_credential("ANALYTICS_DB_USER")
        jdbc_pass = get_credential("ANALYTICS_DB_PASS")

        db_analytics = MySQL(
            spark=spark(),
            jdbc_url=jdbc_url,
            jdbc_user=jdbc_user,
            jdbc_pass=jdbc_pass,
        )

        schema = StructType(
            [
                StructField("id", IntegerType(), nullable=False),
                StructField("name", StringType(), nullable=False),
                StructField("role", StringType(), nullable=False),
                StructField("created_at", TimestampType(), nullable=False),
                StructField("updated_at", TimestampType(), nullable=False),
                StructField("deleted_at", TimestampType(), nullable=True),
            ]
        )

        df = spark().createDataFrame([], schema)

        table = "databricks_test2"

        df_analytics = db_analytics.create(table, df)

        self.assertEqual(df_analytics, True)

    def test_mysql_insert(self):
        jdbc_url = get_credential("ANALYTICS_DB_JDBC")
        jdbc_user = get_credential("ANALYTICS_DB_USER")
        jdbc_pass = get_credential("ANALYTICS_DB_PASS")

        db_analytics = MySQL(
            spark=spark(),
            jdbc_url=jdbc_url,
            jdbc_user=jdbc_user,
            jdbc_pass=jdbc_pass,
        )

        data = [
            ("John", "Developer"),
            ("Jessica", "Analyst"),
            ("Adam", "Manager"),
            ("Henry", "Retired"),
        ]

        schema = ["name", "role"]

        df = spark().createDataFrame(data, schema)

        table = "databricks_test"

        df_analytics = db_analytics.save(table, df)

        self.assertEqual(df_analytics, True)

    def test_mysql_spark_select(self):
        jdbc_url = get_credential("ANALYTICS_DB_JDBC")
        jdbc_user = get_credential("ANALYTICS_DB_USER")
        jdbc_pass = get_credential("ANALYTICS_DB_PASS")

        print("jdbc: ", jdbc_url, jdbc_user, jdbc_pass)

        print("spark: ", spark)

        db_analytics = MySQL(
            spark=spark(),
            jdbc_url=jdbc_url,
            jdbc_user=jdbc_user,
            jdbc_pass=jdbc_pass,
        )

        print("db: ", db_analytics.describe())

        query = """
            SELECT
                role AS "role",
                COUNT(*) AS "#"
            FROM
                databricks_test
            GROUP BY
                role
            ORDER BY
                COUNT(*) DESC
        """

        df_analytics = db_analytics.select(query)

        print(df_analytics)

        self.assertEqual(df_analytics.count() > 0, True)
