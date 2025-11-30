# app/filters/date_filters.py
from datetime import datetime, date
from email.utils import parsedate_to_datetime

def format_date(value):
    if not value:
        return "-"

    if isinstance(value, (datetime, date)):
        return value.strftime("%Y/%m/%d %H:%M")

    s = str(value)

    try:
        dt = parsedate_to_datetime(s)
        return dt.strftime("%Y/%m/%d %H:%M")
    except Exception:
        pass

    try:
        dt = datetime.fromisoformat(s)
        return dt.strftime("%Y/%m/%d %H:%M")
    except Exception:
        pass

    return s
