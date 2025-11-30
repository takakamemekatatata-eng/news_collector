# app/utils/date_utils.py

from datetime import datetime, date, timezone
from email.utils import parsedate_to_datetime

def parse_date_safe(value):
    """RSSやISOの文字列を安全にdatetime(UTC)へ変換する"""
    if not value:
        return None

    # 1. RFC822 (例: "Fri, 21 Nov 2025 18:10:00 +0900")
    try:
        dt = parsedate_to_datetime(value)
        return dt.astimezone(timezone.utc)
    except Exception:
        pass

    # 2. ISO形式 (例: 2025-11-21T18:10:00+09:00)
    try:
        dt = datetime.fromisoformat(value)

        # タイムゾーンなしの場合 → UTC 付与して整合性
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)

        return dt.astimezone(timezone.utc)
    except Exception:
        pass

    # どうしてもパースできない場合
    return None
