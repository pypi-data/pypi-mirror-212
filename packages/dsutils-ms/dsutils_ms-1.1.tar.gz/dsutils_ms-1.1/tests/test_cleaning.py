from unittest import TestCase

from dsutils_ms.helpers.cleaning import (
    drop_duplicates,
    fill_na,
    drop_na,
    trim_spaces,
    underscore_data,
    remove_characters,
    remove_accents,
    clean_columns,
    remove_stop_words,
    replace_data,
    convert_to_na,
)

from fixtures.spark import spark


class TestDataCleaning(TestCase):
    def test_cleaning_drop_duplicates(self):
        columns = ["Name", "Age", "Job"]
        data = [
            ("Sophia", 35, "Product Manager"),
            ("James", 40, "CEO"),
            ("Sophia", 30, "Product Manager"),
            ("Sophia", 35, "Product Manager"),
            ("Sophia", 35, "Product Manager"),
        ]
        df = spark().createDataFrame(data, columns)

        result = [
            ("Sophia", 35, "Product Manager"),
            ("James", 40, "CEO"),
            ("Sophia", 30, "Product Manager"),
        ]
        df_result = spark().createDataFrame(result, columns)

        df = drop_duplicates(df)

        self.assertEqual(df.columns, df_result.columns)
        self.assertEqual(df.dtypes, df_result.dtypes)
        self.assertEqual(df.collect(), df_result.collect())

    def test_cleaning_fill_na(self):
        columns = ["Name", "Age", "Job"]
        data = [
            ("Sophia", 35, "Product Manager"),
            ("James", 40, None),
            ("Sophia", None, "Product Manager"),
            ("Sophia", 35, "Product Manager"),
            (None, 35, "Product Manager"),
        ]
        df = spark().createDataFrame(data, columns)

        result = [
            ("Sophia", 35, "Product Manager"),
            ("James", 40, "x"),
            ("Sophia", -1, "Product Manager"),
            ("Sophia", 35, "Product Manager"),
            ("x", 35, "Product Manager"),
        ]
        df_result = spark().createDataFrame(result, columns)

        df = fill_na(df, "x", subset=["Name", "Job"])
        df = fill_na(df, -1, subset=["Age"])

        self.assertEqual(df.columns, df_result.columns)
        self.assertEqual(df.dtypes, df_result.dtypes)
        self.assertEqual(df.collect(), df_result.collect())

    def test_cleaning_drop_na(self):
        columns = ["Name", "Age", "Job"]
        data = [
            ("Sophia", 35, "Product Manager"),
            ("James", 40, None),
            ("Sophia", None, "Product Manager"),
            ("Sophia", 35, "Product Manager"),
            (None, 35, "Product Manager"),
        ]
        df = spark().createDataFrame(data, columns)

        result = [
            ("Sophia", 35, "Product Manager"),
            ("Sophia", 35, "Product Manager"),
        ]
        df_result = spark().createDataFrame(result, columns)

        df = drop_na(df)

        self.assertEqual(df.columns, df_result.columns)
        self.assertEqual(df.dtypes, df_result.dtypes)
        self.assertEqual(df.collect(), df_result.collect())

    def test_cleaning_trim_spaces_header(self):
        columns = [" Name ", " Age", "Job     Title"]
        data = [
            (" Sophia ", 35, " Product Manager "),
        ]
        df = spark().createDataFrame(data, columns)

        columns = ["Name", "Age", "Job Title"]
        result = [
            (" Sophia ", 35, " Product Manager "),
        ]
        df_result = spark().createDataFrame(result, columns)

        df = trim_spaces(df, how="columns")

        self.assertEqual(df.columns, df_result.columns)
        self.assertEqual(df.dtypes, df_result.dtypes)
        self.assertEqual(df.collect(), df_result.collect())

    def test_cleaning_trim_spaces_data(self):
        columns = [" Name ", " Age", "Job "]
        data = [
            (" Sophia   ", 35, " Product       Manager    "),
        ]
        df = spark().createDataFrame(data, columns)

        result = [
            ("Sophia", 35, "Product Manager"),
        ]
        df_result = spark().createDataFrame(result, columns)

        df = trim_spaces(df, how="data")

        self.assertEqual(df.columns, df_result.columns)
        self.assertEqual(df.dtypes, df_result.dtypes)
        self.assertEqual(df.collect(), df_result.collect())

    def test_cleaning_underscore_header(self):
        columns = ["Full Name", "Age", "Job Title"]
        data = [
            ("Sophia Guedes", 35, "Product Manager"),
            ("James Souza", 40, "Data Scientist"),
            ("João Silva", 30, "Product Owner"),
        ]
        df = spark().createDataFrame(data, columns)

        columns = ["full_name", "age", "job_title"]
        result = [
            ("Sophia Guedes", 35, "Product Manager"),
            ("James Souza", 40, "Data Scientist"),
            ("João Silva", 30, "Product Owner"),
        ]
        df_result = spark().createDataFrame(result, columns)

        df = underscore_data(df, how="columns")

        self.assertEqual(df.columns, df_result.columns)
        self.assertEqual(df.dtypes, df_result.dtypes)
        self.assertEqual(df.collect(), df_result.collect())

    def test_cleaning_underscore_data(self):
        columns = ["Full Name", "Age", "Job Title"]
        data = [
            ("Sophia Guedes", 35, "Product Manager"),
            ("James Souza", 40, "Data Scientist"),
            ("João Silva", 30, "Product Owner"),
        ]
        df = spark().createDataFrame(data, columns)

        result = [
            ("sophia_guedes", 35, "product_manager"),
            ("james_souza", 40, "data_scientist"),
            ("joão_silva", 30, "product_owner"),
        ]
        df_result = spark().createDataFrame(result, columns)

        df = underscore_data(df, how="data")

        self.assertEqual(df.columns, df_result.columns)
        self.assertEqual(df.dtypes, df_result.dtypes)
        self.assertEqual(df.collect(), df_result.collect())

    def test_cleaning_remove_characters_header(self):
        columns = ["Full/Name", "Age?", "Job!Title"]
        data = [
            ("Sophia Guedes", 35, "Product Manager"),
            ("James Souza", 40, "Data Scientist"),
            ("João Silva", 30, "Product Owner"),
        ]
        df = spark().createDataFrame(data, columns)

        columns = ["FullName", "Age", "JobTitle"]
        result = [
            ("Sophia Guedes", 35, "Product Manager"),
            ("James Souza", 40, "Data Scientist"),
            ("João Silva", 30, "Product Owner"),
        ]
        df_result = spark().createDataFrame(result, columns)

        df = remove_characters(df, how="columns")

        self.assertEqual(df.columns, df_result.columns)
        self.assertEqual(df.dtypes, df_result.dtypes)
        self.assertEqual(df.collect(), df_result.collect())

    def test_cleaning_remove_characters_data(self):
        columns = ["FullName", "Age", "JobTitle"]
        data = [
            ("Sophia!Guedes", 35, "Product!Manager"),
            ("James/Souza", 40, "Data&Scientist"),
            ("João?Silva", 30, "Product@Owner"),
        ]
        df = spark().createDataFrame(data, columns)

        result = [
            ("SophiaGuedes", 35, "ProductManager"),
            ("JamesSouza", 40, "DataScientist"),
            ("JoãoSilva", 30, "ProductOwner"),
        ]
        df_result = spark().createDataFrame(result, columns)

        df = remove_characters(df, how="data")

        self.assertEqual(df.columns, df_result.columns)
        self.assertEqual(df.dtypes, df_result.dtypes)
        self.assertEqual(df.collect(), df_result.collect())

    def test_cleaning_remove_accents_header(self):
        columns = [
            "NAÁÀÂÃEÉÈÊUÚÙÛCÇaáàâãeéèême",
            "AIÍÌÎOÓÒÔÕge",
            "JobiíìîoóòôõuúùûcçTitle",
        ]
        data = [
            ("Sophia Guedes", 35, "Product Manager"),
            ("James Souza", 40, "Data Scientist"),
            ("João Silva", 30, "Product Owner"),
        ]
        df = spark().createDataFrame(data, columns)

        columns = [
            "NAAAAAEEEEUUUUCCaaaaaeeeeme",
            "AIIIIOOOOOge",
            "JobiiiiooooouuuuccTitle",
        ]
        result = [
            ("Sophia Guedes", 35, "Product Manager"),
            ("James Souza", 40, "Data Scientist"),
            ("João Silva", 30, "Product Owner"),
        ]
        df_result = spark().createDataFrame(result, columns)

        df = remove_accents(df, how="columns")

        self.assertEqual(df.columns, df_result.columns)
        self.assertEqual(df.dtypes, df_result.dtypes)
        self.assertEqual(df.collect(), df_result.collect())

    def test_cleaning_remove_accents_data(self):
        columns = ["FullName", "Age", "JobTitle"]
        data = [
            ("SophiaAÁÀÂÃEÉÈÊUÚÙÛGuedes", 35, "ProductOÓÒÔÕManager"),
            ("JamesiíìîoóòôõuúùûcçSouza", 40, "DataCÇaáàâãeéèêScientist"),
            ("JoãoIÍÌÎOÓÒÔÕSilva", 30, "ProductáàâãeéOwner"),
        ]
        df = spark().createDataFrame(data, columns)

        result = [
            ("SophiaAAAAAEEEEUUUUGuedes", 35, "ProductOOOOOManager"),
            ("JamesiiiiooooouuuuccSouza", 40, "DataCCaaaaaeeeeScientist"),
            ("JoaoIIIIOOOOOSilva", 30, "ProductaaaaeeOwner"),
        ]
        df_result = spark().createDataFrame(result, columns)

        df = remove_accents(df, how="data")

        self.assertEqual(df.columns, df_result.columns)
        self.assertEqual(df.dtypes, df_result.dtypes)
        self.assertEqual(df.collect(), df_result.collect())

    def test_cleaning_remove_stop_words_header(self):
        columns = [
            "Full me ME ao AO Name",
            "Did did DID para PARA Age",
            "Job when WHEN WhEn esse ESSES Title",
        ]
        data = [
            ("Sophia Guedes", 35, "Product Manager"),
            ("James Souza", 40, "Data Scientist"),
            ("João Silva", 30, "Product Owner"),
        ]
        df = spark().createDataFrame(data, columns)

        columns = ["Full Name", "Age", "Job Title"]
        result = [
            ("Sophia Guedes", 35, "Product Manager"),
            ("James Souza", 40, "Data Scientist"),
            ("João Silva", 30, "Product Owner"),
        ]
        df_result = spark().createDataFrame(result, columns)

        df = remove_stop_words(df, how="columns")

        self.assertEqual(df.columns, df_result.columns)
        self.assertEqual(df.dtypes, df_result.dtypes)
        self.assertEqual(df.collect(), df_result.collect())

    def test_cleaning_convert_to_na(self):
        columns = [" Name ", " Age", "Job "]
        data = [
            ("nan", 35, "Teste1"),
            ("Teste2", 35, "null"),
            ("", 35, "Teste3"),
            ("Teste4", 35, " "),
        ]
        df = spark().createDataFrame(data, columns)

        result = [
            (None, 35, "Teste1"),
            ("Teste2", 35, None),
            (None, 35, "Teste3"),
            ("Teste4", 35, None),
        ]
        df_result = spark().createDataFrame(result, columns)

        df = convert_to_na(df)

        self.assertEqual(df.columns, df_result.columns)
        self.assertEqual(df.dtypes, df_result.dtypes)
        self.assertEqual(df.collect(), df_result.collect())

    def test_cleaning_replace_data_header_1(self):
        columns = [
            "De 1-5, sendo 1 muito insatisfeito",
            "Age, Years",
            "Job.  Title",
        ]
        data = [
            ("Sophia Guedes", 35, "Product Manager"),
            ("James Souza", 40, "Data Scientist"),
            ("João Silva", 30, "Product Owner"),
        ]
        df = spark().createDataFrame(data, columns)

        columns = [
            "De 1-5 sendo 1 muito insatisfeito",
            "Age Years",
            "Job  Title",
        ]
        result = [
            ("Sophia Guedes", 35, "Product Manager"),
            ("James Souza", 40, "Data Scientist"),
            ("João Silva", 30, "Product Owner"),
        ]
        df_result = spark().createDataFrame(result, columns)

        df = replace_data(df, how="columns")

        self.assertEqual(df.columns, df_result.columns)
        self.assertEqual(df.dtypes, df_result.dtypes)
        self.assertEqual(df.collect(), df_result.collect())

    def test_cleaning_replace_data_header_2(self):
        columns = [
            "pais",
            "resistencia_ao_acamamento_(1_a_5)",
            "septoriose__mancha_parda",
        ]
        data = [
            ("Sophia Guedes", 35, "Product Manager"),
            ("James Souza", 40, "Data Scientist"),
            ("João Silva", 30, "Product Owner"),
        ]
        df = spark().createDataFrame(data, columns)

        columns = [
            "country",
            "lodging_resistance",
            "septoria_leaf_spot",
        ]
        result = [
            ("Sophia Guedes", 35, "Product Manager"),
            ("James Souza", 40, "Data Scientist"),
            ("João Silva", 30, "Product Owner"),
        ]
        df_result = spark().createDataFrame(result, columns)

        df = replace_data(
            df,
            how="columns",
            replace_dict={
                "pais": "country",
                "resistencia_ao_acamamento_(1_a_5)": "lodging_resistance",
                "septoriose__mancha_parda": "septoria_leaf_spot",
            },
        )

        self.assertEqual(df.columns, df_result.columns)
        self.assertEqual(df.dtypes, df_result.dtypes)
        self.assertEqual(df.collect(), df_result.collect())

    def test_cleaning_clean_columns_1(self):
        columns = [
            "  NAÁÀÂÃEÉÈÊU/ÚÙÛ CÇaáàâãeéèême ",
            " AIÍÌÎ OÓÒ?ÔÕge  ",
            "     Jobií!ìîoóòôõ   uúùûc+çTitle    ",
        ]
        data = [
            ("Sophia Guedes", 35, "Product Manager"),
            ("James Souza", 40, "Data Scientist"),
            ("João Silva", 30, "Product Owner"),
        ]
        df = spark().createDataFrame(data, columns)

        columns = [
            "naaaaaeeeeuuuu_ccaaaaaeeeeme",
            "aiiii_oooooge",
            "jobiiiiooooo_uuuucctitle",
        ]
        result = [
            ("Sophia Guedes", 35, "Product Manager"),
            ("James Souza", 40, "Data Scientist"),
            ("João Silva", 30, "Product Owner"),
        ]
        df_result = spark().createDataFrame(result, columns)

        df = clean_columns(df)

        self.assertEqual(df.columns, df_result.columns)
        self.assertEqual(df.dtypes, df_result.dtypes)
        self.assertEqual(df.collect(), df_result.collect())

    def test_cleaning_clean_columns_2(self):
        columns = [
            "   De 1-5, sendo 1 muito insatisfeito e 5 muito satisfeito, quanto você está satisfeito com o acompanhamento via WhatsApp ou ligação do time de Sucesso do Cliente?  ",
            " Carimbo de data/hora  ",
            "     Qual o e-mail que. Você utiliza para acessar a plataforma?    ",
        ]
        data = [
            ("Sophia Guedes", 35, "Product Manager"),
            ("James Souza", 40, "Data Scientist"),
            ("João Silva", 30, "Product Owner"),
        ]
        df = spark().createDataFrame(data, columns)

        columns = [
            "15_sendo_1_insatisfeito_5_satisfeito_quanto_satisfeito_acompanhamento_via_whatsapp_ligacao_time_sucesso_cliente",
            "carimbo_datahora",
            "email_utiliza_acessar_plataforma",
        ]
        result = [
            ("Sophia Guedes", 35, "Product Manager"),
            ("James Souza", 40, "Data Scientist"),
            ("João Silva", 30, "Product Owner"),
        ]
        df_result = spark().createDataFrame(result, columns)

        df = clean_columns(df)

        self.assertEqual(df.columns, df_result.columns)
        self.assertEqual(df.dtypes, df_result.dtypes)
        self.assertEqual(df.collect(), df_result.collect())
