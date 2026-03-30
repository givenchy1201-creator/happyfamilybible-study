"""
build_index.py
掃描 bible/ groups/ devotion/ media/ 資料夾，
從每個 HTML 的 <title> 抓取標題，
自動更新 index.html 裡對應的 <ul> 清單。
"""

import os
import re

CATEGORIES = [
    ("bible",   "list-bible"),
    ("groups",  "list-groups"),
    ("devotion","list-devotion"),
    ("media",   "list-media"),
]

EMPTY_NOTE = '<li><span class="empty-note">（尚無內容，敬請期待）</span></li>'


def get_title(filepath):
    """從 HTML 檔案的 <title> 標籤取得標題。"""
    try:
        with open(filepath, encoding="utf-8") as f:
            content = f.read(2000)
        m = re.search(r"<title>(.*?)</title>", content, re.IGNORECASE)
        if m:
            return m.group(1).strip()
    except Exception:
        pass
    return os.path.basename(filepath)


def build_list_html(folder, list_id):
    """掃描資料夾，產生 <ul id="..."> 的內部 HTML。"""
    if not os.path.isdir(folder):
        return EMPTY_NOTE

    files = sorted([
        f for f in os.listdir(folder)
        if f.endswith(".html")
    ])

    if not files:
        return EMPTY_NOTE

    items = []
    for filename in files:
        filepath = os.path.join(folder, filename)
        title = get_title(filepath)
        href = f"{folder}/{filename}"
        items.append(
            f'    <li class="article-item">'
            f'<a href="{href}">{title}</a></li>'
        )

    return "\n".join(items)


def update_index(index_path="index.html"):
    with open(index_path, encoding="utf-8") as f:
        content = f.read()

    for folder, list_id in CATEGORIES:
        items_html = build_list_html(folder, list_id)

        # 取代 <ul id="list-xxx"> 和 </ul> 之間的內容
        pattern = (
            rf'(<ul class="article-list" id="{list_id}">)'
            rf'.*?'
            rf'(</ul>)'
        )
        replacement = rf'\1\n{items_html}\n  \2'
        content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(content)

    print("✅ index.html 已更新")


if __name__ == "__main__":
    update_index()
