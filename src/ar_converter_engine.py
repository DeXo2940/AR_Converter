from typing import Type
from warnings import catch_warnings, simplefilter
# noinspection PyUnresolvedReferences
from openpyxl import Workbook
from pandas import read_excel, ExcelWriter, to_datetime, concat, DataFrame

import columns_languages_enum as columns


class ArConverter:
    DASH_COLUMN = 'DashCount'
    _columns: Type[columns.AbstractColumns] = object
    _column_list = []
    _excel_data = object
    _input_file_path = ''
    _output_file_path = ''

    def __init__(self, input_file, output_file):
        self._input_file_path = input_file
        self._output_file_path = output_file

    @staticmethod
    def create(input_file_path, output_file_path):
        return ArConverter(input_file_path, output_file_path)

    def _open_excel_file(self):
        with catch_warnings(record=True):
            simplefilter("always")
            self._excel_data = read_excel(self._input_file_path, engine="openpyxl")

    def _set_columns_language(self):
        self._columns = columns.ColumnsEN if columns.ColumnsEN.DATE.value in self._excel_data else columns.ColumnsPL
        self._column_list = [self._columns.DATE.value,
                             self._columns.TASK_GROUP.value,
                             self._columns.TASK.value,
                             self._columns.TIME.value,
                             self._columns.DESCRIPTION.value]

    def _keep_only_columns_from_list(self):
        self._excel_data = self._excel_data[self._column_list]

    def _save_excel_file(self):
        writer = ExcelWriter(self._output_file_path, engine='openpyxl')
        self._excel_data.to_excel(writer, sheet_name='Export', index=False)
        writer.save()

    def _remove_holiday(self):
        self._excel_data = self._excel_data.loc[self._excel_data[self._columns.TASK_GROUP.value] != 'Holiday']

    # Remove all single "Other" with less than 8h
    def _remove_other(self):
        self._excel_data = self._excel_data[~self._excel_data.isin(
            self._excel_data.loc[(self._excel_data[self._columns.DESCRIPTION.value] == 'Other') &
                                 (self._excel_data[self._columns.TIME.value] != 8)])[self._columns.DATE.value]]

    def _add_column_with_dash_count(self):
        self._excel_data[self.DASH_COLUMN] = self._excel_data[self._columns.DESCRIPTION.value].apply(
            lambda x: str(x).count('-')
        )

    def _reset_columns(self):
        self._excel_data = self._excel_data[self._column_list]

    def _sort_by_date_and_descriptions(self):
        self._add_column_with_dash_count()

        self._excel_data = self._excel_data.sort_values(
            by=[self._columns.DATE.value, self.DASH_COLUMN, self._columns.TIME.value], ascending=[True, False, True])

        self._reset_columns()

    def _concatenate_descriptions(self):
        # Concatenate descriptions with ','
        self._excel_data[self._columns.DESCRIPTION.value] = self._excel_data.groupby(
            [self._columns.DATE.value,
             self._columns.TASK_GROUP.value,
             self._columns.TASK.value])[self._columns.DESCRIPTION.value].transform(lambda x: ', '.join(x))

    def _set_reporting_time(self):
        self._excel_data[self._columns.TIME.value] = 8

    def _drop_duplicates_sort_and_fix_index(self):
        self._excel_data = self._excel_data.drop_duplicates().sort_values(
            by=self._columns.DATE.value).reset_index()[self._column_list]

    def _rename_columns(self):
        self._columns = columns.ColumnsEN
        self._column_list = [self._columns.DATE.value,
                             self._columns.TASK_GROUP.value,
                             self._columns.TASK.value,
                             self._columns.TIME.value,
                             self._columns.DESCRIPTION.value]
        self._excel_data.columns = self._column_list

    def _shorten_date(self):
        self._excel_data[self._columns.DATE.value] = to_datetime(self._excel_data[self._columns.DATE.value]).dt.date

    def _add_sum_of_times(self):
        self._excel_data = concat(
            [self._excel_data,
             DataFrame({self._columns.TIME.value: [self._excel_data[self._columns.TIME.value].sum()]})],
            ignore_index=True, axis=0)

    def _modify_descriptions(self):
        self._excel_data[self._columns.DESCRIPTION.value] = self._excel_data[self._columns.DESCRIPTION.value].apply(
            lambda x: ' '.join(str(x).replace(',other', '').replace(', other', '').replace(',Other', '').replace(
                ', Other', '').replace('other,', '').replace('other ,', '').replace('Other,', '').replace(
                'Other ,', '').replace(',', ', ').replace(' ,', ', ').split()))

    def convert_AR(self):
        try:
            self._open_excel_file()
            self._set_columns_language()
            self._keep_only_columns_from_list()
            self._remove_holiday()
            self._remove_other()
            self._sort_by_date_and_descriptions()
            self._concatenate_descriptions()
            self._set_reporting_time()
            self._drop_duplicates_sort_and_fix_index()
            self._shorten_date()
            self._modify_descriptions()
            self._rename_columns()
            self._add_sum_of_times()
            self._save_excel_file()
        except OSError as os_error:
            print("OS Error occurred: {}".format(os_error))


def convert(input_file_path, output_file_path):
    ar_converter = ArConverter.create(input_file_path, output_file_path)
    ar_converter.convert_AR()
