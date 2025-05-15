from pathlib import Path

from etl.extract import extract_csv_data, extract_fund_info


def test_extract_fund_info() -> None:
    sample = "Fund Whitestone.28-02-2023 - details"
    name, date = extract_fund_info(sample)
    assert name == "Whitestone"
    assert date == "02/28/2023"


def test_extract_csv_data(tmp_path: Path) -> None:
    csv_content = "price,market value,quantity\n100.5,1000,10"
    csv_file = tmp_path / "Applebead.30-04-2023.csv"
    csv_file.write_text(csv_content)

    df = extract_csv_data(csv_file)
    assert "fund_name" in df.columns
    assert "position_date" in df.columns
    assert df["fund_name"].iloc[0] == "Applebead"
    assert df["position_date"].iloc[0] == "04/30/2023"
