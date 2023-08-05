from unittest import TestCase

from dsutils_ms.adapters.s3 import S3
from dsutils_ms.helpers.env import get_credential

from fixtures.spark import spark


class TestS3(TestCase):
    def test_s3_upload_csv(self):
        AWS_S3_BUCKET = get_credential("AWS_S3_BUCKET")

        data = [
            ("Emily", 25, "Data Scientist"),
            ("Michael", 30, "Engineer"),
        ]

        df = spark().createDataFrame(data, ["Name", "Age", "Job"])

        output_path = "tests/sample.csv"

        df_s3 = S3(spark=spark(), S3_bucket=AWS_S3_BUCKET).upload(
            output_path, df
        )

        self.assertEqual(df_s3, True)

    def test_s3_upload_json(self):
        AWS_S3_BUCKET = get_credential("AWS_S3_BUCKET")

        data = [
            ("Sophia", 35, "Product Manager"),
            ("James", 40, "CEO"),
        ]

        df = spark().createDataFrame(data, ["Name", "Age", "Job"])

        output_path = "tests/sample.json"

        df_s3 = S3(spark=spark(), S3_bucket=AWS_S3_BUCKET).upload(
            output_path, df
        )

        self.assertEqual(df_s3, True)

    def test_s3_upload_parquet(self):
        AWS_S3_BUCKET = get_credential("AWS_S3_BUCKET")

        data = [
            ("Liam", 24, "Marketing Manager"),
            ("Olivia", 29, "Designer"),
        ]

        df = spark().createDataFrame(data, ["Name", "Age", "Job"])

        output_path = "tests/sample.parquet"

        df_s3 = S3(spark=spark(), S3_bucket=AWS_S3_BUCKET).upload(
            output_path, df
        )

        self.assertEqual(df_s3, True)

    def test_s3_read_csv(self):
        AWS_S3_BUCKET = get_credential("AWS_S3_BUCKET")

        input_path = "tests/sample.csv"

        df = S3(spark=spark(), S3_bucket=AWS_S3_BUCKET).download(input_path)

        self.assertEqual(df.count() > 0, True)

    def test_s3_read_json(self):
        AWS_S3_BUCKET = get_credential("AWS_S3_BUCKET")

        input_path = "tests/sample.json"

        df = S3(spark=spark(), S3_bucket=AWS_S3_BUCKET).download(input_path)

        self.assertEqual(df.count() > 0, True)

    def test_s3_read_parquet(self):
        AWS_S3_BUCKET = get_credential("AWS_S3_BUCKET")

        input_path = "tests/sample.parquet"

        df = S3(spark=spark(), S3_bucket=AWS_S3_BUCKET).download(input_path)

        self.assertEqual(df.count() > 0, True)
