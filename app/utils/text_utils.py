# app/utils/text.py
import re

def strip_html_tags(text):
    if not text:
        return ""
    # HTMLタグを除去
    clean = re.sub('<[^<]+?>', '', text)
    # 余計な空白を整理
    clean = re.sub('\s+', ' ', clean).strip()
    return clean
