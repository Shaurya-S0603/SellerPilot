from pathlib import Path
from etl.detector import ReportDetector
folder = Path("data/temp")

for file in folder.iterdir():
    if file.is_file():
        report = ReportDetector.detect(file)
        print(file.name, "->", report.value)