# from dsutils_ms.src.helpers.log import log_end_result, log_title
# from dsutils_ms.src.adapters.google_sheets import GoogleSheets


# def gs_load_concat(
#     auth, spreadsheet, sheets, subset=None, dropna=True, trim_spaces=True
# ) -> pd.DataFrame:
#     df = pd.DataFrame()
#     for sheet in sheets:
#         df_sheet = GoogleSheets(auth, spreadsheet, sheet).load(
#             subset=subset, dropna=dropna, trim_spaces=trim_spaces
#         )
#         df = pd.concat([df, df_sheet]).reset_index(drop=True)
#     return df


# def df_unique_data(df):
#     log_title("Unique Data")
#     for column in df.columns:
#         log_end_result(
#             column,
#             df[column].unique(),
#             show_datetime=False,
#             show_separator=False,
#         )
