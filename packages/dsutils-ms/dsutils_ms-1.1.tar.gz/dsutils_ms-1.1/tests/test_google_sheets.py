from unittest import TestCase

from dsutils_ms.adapters.google_sheets import GoogleSheets
from dsutils_ms.helpers.env import get_credential

from fixtures.spark import spark


class TestGoogleSheets(TestCase):
    def test_google_sheets_load(self):
        credential = get_credential("GOOGLE_SERVICE_ACCOUNT")
        gs_cultivares = GoogleSheets(
            spark(),
            credential,
            "1fafH94LlCUZEQtfTynf0jw_APboEvAgRtLb-eHoXYSc",
            "Doenças_Soja",
        )

        df_cultivares = gs_cultivares.load()

        print(df_cultivares.show())

        self.assertEqual(df_cultivares.count() > 0, True)

    def test_google_sheets_save_1(self):
        credential = get_credential("GOOGLE_SERVICE_ACCOUNT")
        gs_teste = GoogleSheets(
            spark(),
            credential,
            "1UBZqL1UwvweXxN-PsJw3Ea9ogRSswlyQVi9PfkMXFDs",
            "Teste1",
        )

        data = [
            ("Emily", 25, "Data Scientist"),
            ("Michael", 30, "Engineer"),
        ]

        df = spark().createDataFrame(data, ["Name", "Age", "Job"])

        gs_teste.save(df)

        df_teste = gs_teste.load()

        self.assertEqual(df_teste.count() > 0, True)

    def test_google_sheets_save_2(self):
        credential = get_credential("GOOGLE_SERVICE_ACCOUNT")
        gs_teste = GoogleSheets(
            spark(),
            credential,
            "1UBZqL1UwvweXxN-PsJw3Ea9ogRSswlyQVi9PfkMXFDs",
            "Teste2",
        )

        data = [
            ("Sophia", 35, "Product Manager"),
            ("James", 40, "CEO"),
        ]

        df = spark().createDataFrame(data, ["Name", "Age", "Job"])

        gs_teste.save(df, append=False)

        df_teste = gs_teste.load()

        self.assertEqual(df_teste.count() > 0, True)

    def test_google_sheets_save_3(self):
        credential = get_credential("GOOGLE_SERVICE_ACCOUNT")
        gs_teste = GoogleSheets(
            spark(),
            credential,
            "1UBZqL1UwvweXxN-PsJw3Ea9ogRSswlyQVi9PfkMXFDs",
            "Teste3",
        )

        data = [
            ("Liam", 24, "Marketing Manager"),
            ("Olivia", 29, "Designer"),
        ]

        df = spark().createDataFrame(data, ["Name", "Age", "Job"])

        gs_teste.save(df, resize=False)

        df_teste = gs_teste.load()

        self.assertEqual(df_teste.count() > 0, True)

    def test_google_sheets_save_4(self):
        credential = get_credential("GOOGLE_SERVICE_ACCOUNT")
        gs_teste = GoogleSheets(
            spark(),
            credential,
            "1UBZqL1UwvweXxN-PsJw3Ea9ogRSswlyQVi9PfkMXFDs",
            "Teste4",
        )

        data = [
            ("João", 43, "Marketing Manager"),
            ("Maria", 24, "Designer"),
        ]

        df = spark().createDataFrame(data, ["Name", "Age", "Job"])

        gs_teste.save(df, append=False, resize=False)

        df_teste = gs_teste.load()

        self.assertEqual(df_teste.count() > 0, True)
