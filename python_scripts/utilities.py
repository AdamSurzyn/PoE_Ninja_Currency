from datetime import datetime
import re

def format_sample_time(time_str):
    sample_time_iso = re.sub(r"\.\d+Z", "", time_str)
    sample_time_utc = datetime.fromisoformat(sample_time_iso)
    sample_time_hour = sample_time_utc.replace(minute=0, second=0, microsecond=0)
    return sample_time_hour