import re
from pathlib import Path

import pdfplumber

from src.utilize.logger import get_log


logger = get_log(__name__)

# English text inside the last pair of brackets: 'Ngày giao dịch (Trade date)' -> 'Trade date'
ENGLISH_NAME_PATTERN = re.compile(r'\(([^()]*)\)\s*$')


class PdfReader:
    # Reads the trade table of a PDF file and returns its rows as dictionaries.
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

        # Fail early with a clear message instead of a pdfplumber error later.
        if not self.file_path.is_file():
            raise FileNotFoundError(f'PDF file not found: {self.file_path}')

    def read_data(self) -> list:
        # Return every trade row of the PDF as a dict: {English column name: cell value}.
        # Example: [{'No': '1', 'Trade date': '23/11/2026', 'Order type': 'Mua(Buy)', ...}, ...]
        data = []
        header = None

        with pdfplumber.open(self.file_path) as pdf:
            for page in pdf.pages:
                for table in page.extract_tables():
                    rows = [self._clean_row(row) for row in table]

                    # A table that continues on the next page may have no header,
                    # so the header of the previous page is reused.
                    if rows and self._is_header_row(rows[0]):
                        header = [self._english_name(cell) for cell in rows[0]]
                        rows = rows[1:]

                    if header is None:
                        # No header seen yet: this is not the trade table.
                        continue

                    for row in rows:
                        # Skip empty rows and the 'Tổng cộng' (total) row.
                        if any(row) and not self._is_total_row(row):
                            data.append(dict(zip(header, row)))

        logger.info(f'{self.file_path.name}: {len(data)} rows read')
        return data

    @staticmethod
    def _clean_row(row: list) -> list:
        # pdfplumber returns None for empty cells and '\n' inside wrapped text:
        # 'Ngày giao dịch\n(Trade date)' -> 'Ngày giao dịch (Trade date)'
        return [' '.join((cell or '').split()) for cell in row]

    @staticmethod
    def _is_header_row(row: list) -> bool:
        # The header row of the TCBS table always starts with 'STT (No)'.
        return bool(row) and row[0].startswith('STT')

    @staticmethod
    def _is_total_row(row: list) -> bool:
        # The last row of the table: ['Tổng cộng', '', ..., '80,424']
        return bool(row) and row[0].startswith('Tổng cộng')

    @staticmethod
    def _english_name(header_cell: str) -> str:
        # Keep only the English name in brackets; keep the cell as it is if there is none.
        # 'Ngày giao dịch (Trade date)' -> 'Trade date'
        match = ENGLISH_NAME_PATTERN.search(header_cell)
        return match.group(1).strip() if match else header_cell
