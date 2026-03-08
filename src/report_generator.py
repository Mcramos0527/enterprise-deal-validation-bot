import pandas as pd
from utils import OUTPUT_DIR, ensure_output_dir


def write_change_report(rows: list[dict]) -> str:
    ensure_output_dir()
    output_path = OUTPUT_DIR / "change_report.csv"
    df = pd.DataFrame(rows)
    df.to_csv(output_path, index=False)
    return str(output_path)


def write_execution_log(log_lines: list[str]) -> str:
    ensure_output_dir()
    output_path = OUTPUT_DIR / "execution_log.txt"
    with open(output_path, "w", encoding="utf-8") as file:
        for line in log_lines:
            file.write(line + "\n")
    return str(output_path)