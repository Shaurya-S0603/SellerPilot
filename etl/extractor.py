from pathlib import Path
from zipfile import ZipFile
import shutil
from loguru import logger
from config.settings import RAW_DATA_DIR

TEMP_DIR = RAW_DATA_DIR.parent / "temp"

class ZipExtractor:
    def __init__(self):
        TEMP_DIR.mkdir(parents=True, exist_ok=True)

    def clean_temp(self):
        if TEMP_DIR.exists():
            shutil.rmtree(TEMP_DIR)

        TEMP_DIR.mkdir(parents=True, exist_ok=True)

    def find_zip_files(self):
        return list(RAW_DATA_DIR.glob("*.zip"))

    def extract(self, zip_path: Path):
        logger.info(f"Extracting {zip_path.name}")
        self.clean_temp()

        with ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(TEMP_DIR)

        extracted_files = []
        for file in TEMP_DIR.rglob("*"):

            if file.is_file():

                extracted_files.append(file)

        logger.success(
            f"Extracted {len(extracted_files)} files."
        )

        return extracted_files