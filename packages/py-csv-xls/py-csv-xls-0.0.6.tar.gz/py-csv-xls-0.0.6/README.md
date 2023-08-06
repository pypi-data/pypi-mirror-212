# py-csv-xls

[![PyPI](https://img.shields.io/pypi/v/py-csv-xls)](https://pypi.org/project/py-csv-xls/)
[![License](https://img.shields.io/github/license/pog7x/py-csv-xls)](https://github.com/pog7x/py-csv-xls/blob/master/LICENSE)

## Converter from csv format to xls

### Installation

```bash
pip install py-csv-xls
```

### Example
```python
from py_csv_xls import CSVSniffer, ExcelWorker, PyCsvXlsException

file_lines = CSVSniffer(
    main_path="/abs/path/to/ur/csv/or/dir",
).get_dir_files_with_lines()

ExcelWorker(
    workbook_name="/abs/path/to/ur/xl/without/extension",
    workbook_extension=".xls",
    want_cleared=True,
).fill_workbook(all_data=file_lines)
```