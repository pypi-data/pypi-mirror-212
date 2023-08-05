from dsutils_ms.adapters.interface import ConnectorAdapterInterface

from pyspark.sql import DataFrame

from typing import Any, Dict
import gspread


class GoogleSheets(ConnectorAdapterInterface):
    """``GoogleSheets`` loads / save google spreadsheet data as `PySpark` dataframe.

    Example:
    ::
        >>> GoogleSheets(auth = <json_path>,
                spreadsheet = <spreadsheet_id>,
                sheet = <sheet_name>,
                cell_range = <A1_notation>)
    """

    def __init__(self, spark, auth, spreadsheet, sheet, cell_range=""):
        """Creates a new instance of GoogleSheets to load / save data.

        Args:
            spark: SparkSession.
            auth: The location of the gcp service account key.
            spreadsheet: The google spreadsheet id.
            sheet: the sheet name.
            cell_range: the A1 notation range.
        """

        self._spark = spark
        self._auth = auth
        self._spreadsheet = spreadsheet
        self._sheet = sheet
        self._cell_range = cell_range
        self._rows = 0
        self._cols = 0

        NOTATION_START_CELL = 0
        self._save_start_cell = cell_range.split(":")[NOTATION_START_CELL]

        try:
            gs_service_account = gspread.service_account_from_dict(self._auth)
        except Exception as e:
            raise Exception("Google Service Account Error") from e

        try:
            gs_spreadsheet = gs_service_account.open_by_key(self._spreadsheet)
        except Exception as e:
            raise Exception("Spreadsheet not Found") from e

        try:
            worksheet_exist = False
            for worksheet in gs_spreadsheet.worksheets():
                if self._sheet == worksheet.title:
                    worksheet_exist = True

            if worksheet_exist is False:
                HEADER_SIZE = 1
                gs_spreadsheet.add_worksheet(
                    self._sheet, HEADER_SIZE, HEADER_SIZE
                )
        except Exception as e:
            raise Exception("Add Worksheet Error") from e

        try:
            self._gs_worksheet = gs_spreadsheet.worksheet(self._sheet)
        except Exception as e:
            raise Exception("Worksheet not Found") from e

    def load(self) -> DataFrame:
        """Loads data from the Google Spreadsheets.

        Returns:
            PySpark DataFrame.
        """

        try:
            gs_data = self._gs_worksheet.get(
                self._cell_range,
                value_render_option="UNFORMATTED_VALUE",
                date_time_render_option="FORMATTED_STRING",
            )

            if len(gs_data) <= 1:
                return None
        except Exception as e:
            raise Exception("Worksheet not Found") from e

        try:
            HEADER_ROW = 0
            VALUES_ROWS = 1

            gs_dataframe = self._spark.createDataFrame(
                gs_data[VALUES_ROWS:], gs_data[HEADER_ROW]
            )
        except Exception as e:
            raise Exception("Cell Lookup Error") from e

        try:
            self._rows = int(gs_dataframe.count())
            self._cols = int(len(gs_dataframe.columns))
        except Exception as e:
            raise Exception("Count Rows Error") from e

        return gs_dataframe

    def save(self, data: DataFrame, resize=True, append=True) -> None:
        """Saves PySpark dataframe to the specified google spreadsheet file.

        Args:
            data: PySpark DataFrame to write.
            resize: If True, resize the worksheet to fit the data.
            append: If True, append the data to the existing data.
        """

        self._resize = resize
        self._append = append

        try:
            data_to_write = data
            if self._append:
                original_data = self.load()
                if original_data:
                    data_to_write = original_data.union(data)
        except Exception as e:
            raise Exception("Append Data Error") from e

        try:
            data_header = [data_to_write.columns]
            data_values = [list(row) for row in data_to_write.collect()]
            list_to_write = data_header + data_values
        except Exception as e:
            raise Exception("Convert Data Error") from e

        try:
            self._rows = int(data_to_write.count())
            self._cols = int(len(data_to_write.columns))
        except Exception as e:
            raise Exception("Count Rows Error") from e

        try:
            HEADER_SIZE = 1
            self._rows += HEADER_SIZE

            self._gs_worksheet.update(self._save_start_cell, list_to_write)

            if self._resize:
                self._gs_worksheet.resize(rows=self._rows, cols=self._cols)
        except Exception as e:
            raise Exception("Update Worksheet Error") from e

    def describe(self) -> Dict[str, Any]:
        """Returns a dict that describes the attributes of the dataset.

        Returns:
            Dictionary with all parameters.
        """

        return dict(
            auth=self._auth,
            spreadsheet=self._spreadsheet,
            sheet=self._sheet,
            cell_range=self._cell_range,
            rows=self._rows,
            cols=self._cols,
            append=self._append,
            resize=self._resize,
        )
