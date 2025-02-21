from phi.tools import Toolkit, tool
from phi.utils.log import logger
from src.tools import read_csv, read_excel, read_json, read_txt

class FilePlugin(Toolkit):
    def __init__(self):
        super().__init__(
            name="file_plugin",
        )

        self.register(self.read_csv_file)
        self.register(self.read_excel_file)
        self.register(self.read_json_file)
        self.register(self.read_txt_file)

    def read_csv_file(self, file_path: str) -> str:
        """
        Read a CSV file and return the content
        """
        logger.info(f"Reading CSV file: {file_path}")
        return read_csv(file_path)

    def read_excel_file(self, file_path: str) -> str:
        """
        Read an Excel file and return the content
        """
        logger.info(f"Reading Excel file: {file_path}")
        return read_excel(file_path)

    def read_json_file(self, file_path: str) -> str:
        """
        Read a JSON file and return the content
        """
        logger.info(f"Reading JSON file: {file_path}")
        return read_json(file_path)

    def read_txt_file(self, file_path: str) -> str:
        """
        Read a TXT file and return the content
        """
        logger.info(f"Reading TXT file: {file_path}")
        return read_txt(file_path)
