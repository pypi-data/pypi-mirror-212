import re
from typing import Literal

import nltk
from nltk.corpus import stopwords


from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from pyspark.sql.types import StringType


def convert_to_na(df: DataFrame, strs_to_na=None, subset=None) -> DataFrame:
    if strs_to_na is None:
        strs_to_na = ["", " ", "null", "none", "nan", "None", "NaN"]

    if subset is None:
        subset = df.columns

    for col in subset:
        df = df.withColumn(
            col,
            F.when(
                F.col(col).isin(strs_to_na),
                F.lit(None).cast(df.schema[col].dataType),
            ).otherwise(F.col(col)),
        )

    return df


def drop_duplicates(df: DataFrame, subset=None, convert_na=True) -> DataFrame:
    if convert_na:
        df = convert_to_na(df)
    return df.dropDuplicates(subset)


def fill_na(df: DataFrame, value, subset=None, convert_na=True) -> DataFrame:
    if convert_na:
        df = convert_to_na(df)
    return df.fillna(value, subset)


def drop_na(
    df: DataFrame, how="any", subset=None, convert_na=True
) -> DataFrame:
    if convert_na:
        df = convert_to_na(df)
    return df.dropna(how, subset)


def trim_spaces(
    df: DataFrame, how: Literal["columns", "data"] = "data"
) -> DataFrame:
    """
    Function to trim spaces from DataFrame columns or data.
    """

    if how == "columns":
        df = df.select(
            [F.col(c).alias(re.sub(" +", " ", c.strip())) for c in df.columns]
        )
    elif how == "data":
        string_cols = [
            col_name.name
            for col_name in df.schema.fields
            if isinstance(col_name.dataType, StringType)
        ]

        for col_name in string_cols:
            df = df.withColumn(
                col_name, F.trim(F.regexp_replace(F.col(col_name), " +", " "))
            )
    else:
        raise ValueError("Invalid how parameter. Must be 'columns' or 'data'")
    return df


def underscore_data(
    df: DataFrame, how: Literal["columns", "data"] = "data"
) -> DataFrame:
    """
    Function to underscore DataFrame columns or data.
    """
    if how == "columns":
        df = df.select(
            [F.col(c).alias(c.replace(" ", "_").lower()) for c in df.columns]
        )
    elif how == "data":
        string_cols = [
            col_name.name
            for col_name in df.schema.fields
            if isinstance(col_name.dataType, StringType)
        ]
        for col_name in string_cols:
            df = df.withColumn(
                col_name, F.lower(F.regexp_replace(F.col(col_name), " ", "_"))
            )
    else:
        raise ValueError("Invalid how parameter. Must be 'columns' or 'data'")
    return df


def remove_characters(
    df: DataFrame,
    how: Literal["columns", "data"] = "data",
    characters_to_remove="/?\\!+-$@#%&*()",
) -> DataFrame:
    """
    Function to remove characters from DataFrame columns or data.
    """
    if how == "columns":
        df = df.select(
            [
                F.col(c).alias(
                    c.translate(str.maketrans("", "", characters_to_remove))
                )
                for c in df.columns
            ]
        )
    elif how == "data":
        string_cols = [
            col_name.name
            for col_name in df.schema.fields
            if isinstance(col_name.dataType, StringType)
        ]
        for col_name in string_cols:
            df = df.withColumn(
                col_name,
                F.translate(F.col(col_name), characters_to_remove, ""),
            )
    else:
        raise ValueError("Invalid how parameter. Must be 'columns' or 'data'")
    return df


def remove_accents(
    df: DataFrame, how: Literal["columns", "data"] = "data"
) -> DataFrame:
    """
    Function to remove accents from DataFrame columns or data.
    """
    accents = "AÁÀÂÃEÉÈÊIÍÌÎOÓÒÔÕUÚÙÛCÇaáàâãeéèêiíìîoóòôõuúùûcç"
    non_accents = "AAAAAEEEEIIIIOOOOOUUUUCCaaaaaeeeeiiiiooooouuuucc"

    if how == "columns":
        df = df.select(
            [
                F.col(c).alias(
                    c.translate(str.maketrans(accents, non_accents, ""))
                )
                for c in df.columns
            ]
        )
    elif how == "data":
        string_cols = [
            col_name.name
            for col_name in df.schema.fields
            if isinstance(col_name.dataType, StringType)
        ]
        for col_name in string_cols:
            df = df.withColumn(
                col_name, F.translate(F.col(col_name), accents, non_accents)
            )
    else:
        raise ValueError("Invalid how parameter. Must be 'columns' or 'data'")
    return df


def remove_stop_words(
    df: DataFrame, how: Literal["columns", "data"] = "data"
) -> DataFrame:
    """
    Function to remove stop words from DataFrame columns or data.
    """

    nltk.download("stopwords")

    english_stop_words = stopwords.words("english")
    portuguese_stop_words = stopwords.words("portuguese")
    all_words = english_stop_words + portuguese_stop_words

    if how == "columns":
        cols = []
        for col_name in df.columns:
            new_cols = col_name.split(" ")
            new_cols = list(map(lambda x: re.sub(" +", " ", x), new_cols))
            for c in new_cols:
                new_cols = [c for c in new_cols if c.lower() not in all_words]
            new_cols = " ".join(new_cols)

            cols.append(F.col(col_name).alias(new_cols))

        df = df.select(cols)
    elif how == "data":
        raise ValueError("Not implemented for data yet")
    else:
        raise ValueError("Invalid how parameter. Must be 'columns' or 'data'")
    return df


def replace_data(
    df: DataFrame,
    how: Literal["columns", "data"] = "data",
    replace_dict={", ": " ", ". ": " "},
) -> DataFrame:
    """
    Function to trim spaces from DataFrame columns or data.
    """

    if how == "columns":
        cols = []
        for c in df.columns:
            pattern = re.compile(
                "|".join(re.escape(key) for key in replace_dict.keys())
            )
            new_col = pattern.sub(
                lambda match: replace_dict[match.group(0)], c
            )

            escaped_column_name = "`{}`".format(c)

            cols.append(F.col(escaped_column_name).alias(new_col))
        df = df.select(cols)
    elif how == "data":
        raise ValueError("Not implemented for data yet")
    else:
        raise ValueError("Invalid how parameter. Must be 'columns' or 'data'")
    return df


def clean_columns(
    df: DataFrame,
    replace=True,
    stop_words=True,
    trim=True,
    characters=True,
    accents=True,
    underscore=True,
) -> DataFrame:
    """
    Function to clean DataFrame columns or data.
    """
    if replace:
        df = replace_data(df, how="columns")
    if stop_words:
        df = remove_stop_words(df, how="columns")
    if trim:
        df = trim_spaces(df, how="columns")
    if characters:
        df = remove_characters(df, how="columns")
    if accents:
        df = remove_accents(df, how="columns")
    if underscore:
        df = underscore_data(df, how="columns")

    return df
