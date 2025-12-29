from pathlib import Path

def list_csv_files(data_dir: str) -> list[str]:
    data_path = Path(data_dir).resolve()
    return [str(f) for f in data_path.glob("*.csv")]
