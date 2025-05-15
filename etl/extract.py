import re
from datetime import datetime
from pathlib import Path

import pandas as pd


def extract_fund_info(filename: str) -> tuple[str | None, str | None]:
    line = filename
    line = re.sub(
        r"^(mend-report|Fund|Report-of|rpt|TT_monthly)", "", line, flags=re.IGNORECASE
    )
    line = line.strip(" -_")

    name_match = re.match(r"([A-Za-z\s]+?)(?=[._])", line)
    fund_name = name_match.group(1).strip() if name_match else None

    date_match = re.search(
        r"(\d{2}[-_]\d{2}[-_]\d{4}|\d{8}|\d{4}[-_]\d{2}[-_]\d{2})", line
    )
    raw_date = date_match.group(1) if date_match else None

    if raw_date:
        normalized_date = raw_date.replace("_", "-")
        for fmt in ("%d-%m-%Y", "%m-%d-%Y", "%Y-%m-%d", "%Y%m%d"):
            try:
                date_obj = datetime.strptime(normalized_date, fmt)
                standardized_date = date_obj.strftime("%m/%d/%Y")
                break
            except ValueError:
                standardized_date = None
    else:
        standardized_date = None

    return fund_name, standardized_date


def extract_csv_data(csv_path: Path) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    df.columns = [c.lower().replace(" ", "_").replace("/", "") for c in df.columns]
    fund_name, position_date = extract_fund_info(csv_path.stem)
    df["fund_name"] = fund_name
    df["position_date"] = position_date
    return df
