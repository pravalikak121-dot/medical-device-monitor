from pathlib import Path

import pandas as pd


def generate_device_report(devices: list[dict], output_path: str = "reports/device_health_report.csv") -> str:
    """Generate a CSV report from device data."""
    Path("reports").mkdir(exist_ok=True)

    dataframe = pd.DataFrame(devices)
    dataframe.to_csv(output_path, index=False)

    return output_path
