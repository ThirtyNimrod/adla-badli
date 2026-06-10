"""Data converter group: CSV and JSON sources normalized through pandas."""
from app.converters.data_converters.json_to_xlsx import JsonToXlsxConverter
from app.converters.data_converters.json_to_docx import JsonToDocxConverter
from app.converters.data_converters.json_to_pdf import JsonToPdfConverter
from app.converters.data_converters.json_to_csv import JsonToCsvConverter
from app.converters.data_converters.csv_to_xlsx import CsvToXlsxConverter
from app.converters.data_converters.csv_to_docx import CsvToDocxConverter
from app.converters.data_converters.csv_to_pdf import CsvToPdfConverter
from app.converters.data_converters.csv_to_json import CsvToJsonConverter

DATA_CONVERTERS = [
    JsonToXlsxConverter,
    JsonToDocxConverter,
    JsonToPdfConverter,
    JsonToCsvConverter,
    CsvToXlsxConverter,
    CsvToDocxConverter,
    CsvToPdfConverter,
    CsvToJsonConverter,
]
