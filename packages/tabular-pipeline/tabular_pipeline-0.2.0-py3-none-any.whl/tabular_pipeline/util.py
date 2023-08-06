import csv
import mimetypes
import os
from io import TextIOWrapper


def normalise_entry(entry) -> str:
    return str(entry).lower().strip()


def create_dir(path: str):
    if path and not os.path.exists(path):
        os.mkdir(path)
    return path


def is_xlsx(file_path):
    # get the file extension
    file_ext = normalise_entry(os.path.splitext(file_path)[1])
    if file_ext == ".xlsx":
        # get the file's MIME type
        mime_type, _ = mimetypes.guess_type(file_path)
        if (
            mime_type
            == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        ):
            return True

    return False


def detect_csv_delimiter(text: TextIOWrapper) -> str:
    sample = text.read(4096)
    dialect = csv.Sniffer().sniff(sample)
    return dialect.delimiter
