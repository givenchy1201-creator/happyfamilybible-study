"""
build_index.py
掃描 bible/ 資料夾，依書目分組，
自動生成每本書的索引頁，並更新首頁書目列表。
也處理 groups/ devotion/ media/ 的平面列表。
"""

import os
import re

BOOK_MAP = {
    "genesis":        "創世記",
    "exodus":         "出埃及記",
    "matthew":        "馬太福音",
    "mark":           "馬可福音",
    "luke":           "路加福音",
    "john":           "約翰福音",
    "acts":           "使徒行傳",
    "romans":         "羅馬書",
    "1corinthians":   "哥林多前書",
    "2corinthians":   "哥林多後書",
    "galatians":      "加拉太書",
    "ephesians":      "以弗所書",
    "philippians":    "腓立比書",
    "colossians":     "歌羅西書",
    "1thessalonians": "帖撒羅尼迦前書",
    "2thessalonians": "帖撒羅尼迦後書",
    "1timothy":       "提摩太前書",
    "2timothy":       "提摩太後書",
    "hebrews":        "希伯來書",
    "james":          "雅各書",
    "1peter":         "彼得前書",
    "2peter":         "彼得後書",
    "1john":          "約翰一書",
    "revelation":     "啟示錄",
    "psalms":         "詩篇",
    "proverbs":       "箴言",
}

EMPTY_NOTE = '<li><span class="empty-note">（尚無內容，敬請期待）</span></li>'

PARCHMENT_STYLE = """<link href="https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@400;700&family=Cinzel:wght@400;600;700&family=Noto+Serif+TC:wght@300;400;500;700&display=swap" rel="stylesheet">
<style>
  :root {
    --parchment: #ede8d8; --parchment-dark: #d8ceae; --parchment-deep: #b8a878;
    --ink: #100e08; --ink-faded: #302a1a; --ink-light: #584e38;
    --gold: #9a7808; --gold-mid: #c8a010;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    background-color: #181408;
    background-image: radial-gradient(ellipse at 30% 20%, #28200a 0%, transparent 55%), radial-gradient(ellipse at 70% 80%, #100c04 0%, transparent 55%);
    font-family: 'Noto Serif TC', serif; color: var(--ink); min-height: 100vh; padding: 2rem 1rem;
  }
  .codex-cover {
    max-width: 820px; margin: 0 auto;
    background: linear-gradient(160deg, #2a2408 0%, #141008 100%);
    border: 3px solid #4a3e14; border-radius: 3px; padding: 6px;
    box-shadow: 0 0 0 1px rgba(160,140,40,.25), 8px 12px 40px rgba(0,0,0,.85);
  }
  .codex-page {
    background-color: var(--parchment);
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='400'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.6' numOctaves='4' stitchTiles='stitch'/%3E%3CfeColorMatrix type='saturate' values='0'/%3E%3C/filter%3E%3Crect width='400' height='400' filter='url(%23n)' opacity='0.06'/%3E%3C/svg%3E"), linear-gradient(175deg, rgba(160,140,60,.18) 0%, transparent 15%, transparent 85%, rgba(140,110,40,.15) 100%);
    border: 1px solid var(--parchment-dark); padding: 3rem 3.5rem; position: relative; overflow: hidden;
  }
  .back-link {
    display: inline-flex; align-items: center; gap: 0.4rem;
    font-size: 0.82rem; color: var(--ink-light); text-decoration: none;
    margin-bottom: 1.5rem; letter-spacing: 0.06em; transition: color 0.2s;
  }
  .back-link:hover { color: var(--gold); }
  .page-title {
    font-family: 'Cinzel', serif; font-size: 1.4rem; font-weight: 600;
    color: var(--ink); letter-spacing: 0.1em;
    border-bottom: 1.5px solid var(--parchment-deep); padding-bottom: 1rem; margin-bottom: 2rem;
  }
  .article-list { list-style: none; display: flex; flex-direction: column; gap: 0.5rem; }
  .article-item a {
    display: flex; align-items: center; gap: 0.8rem; padding: 0.65rem 1rem;
    border-radius: 2px; border-left: 2px solid transparent;
    text-decoration: none; color: var(--ink-faded); font-size: 0.95rem;
    letter-spacing: 0.04em; transition: all 0.2s; background: rgba(180,160,80,.04);
  }
  .article-item a:hover { border-left-color: var(--gold); background: rgba(154,120,8,.08); color: var(--ink); padding-left: 1.3rem; }
  .article-item a::before { content: '✦'; font-size: 0.6rem; color: var(--gold-mid); flex-shrink: 0; }
  .codex-footer { text-align: center; margin-top: 3rem; padding-top: 1.5rem; border-top: 1px solid var(--parchment-dark); font-size: 0.78rem; color: var(--ink-light); letter-spacing: 0.08em; }
  .empty-note { font-size: 0.82rem; color: var(--ink-light); font-style: italic; padding: 0.5rem 1rem; opacity: 0.6; }
</style>"""


def get_title(filepath):
    try:
        with open(filepath, encoding="utf-8") as f:
            content = f.read(2000)
        m = re.search(r"<title>(.*?)</title>", content, re.IGNORECASE)
        if m:
            return m.group(1).strip()
    except Exception:
        pass
    return os.path.basename(filepath)


def get_book_prefix(filename):
    return filename.split("_")[0].lower()


def group_bible_files():
    folder = "bible"
    if not os.path.isdir(folder):
        return {}
    files = sorted([f for f in os.listdir(folder) if f.endswith(".html") and "_" in f])
    groups = {}
    for filename in files:
        prefix = get_book_prefix(filename)
        groups.setdefault(prefix, []).append(filename)
    return groups


def generate_book_page(prefix, files, book_name):
    items = []
    for filename in files:
        filepath = os.path.join("bible", filename)
        title = get_title(filepath)
        items.append(f'      <li class="article-item"><a href="{filename}">{title}</a></li>')
    items_html = "\n".join(items)

    return f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{book_name} · 快樂查經班</title>
{PARCHMENT_STYLE}
</head>
<body>
<div class="codex-cover">
<div class="codex-page">
  <a class="back-link" href="../index.html">← 返回首頁</a>
  <div class="page-title">📖 {book_name}</div>
  <ul class="article-list">
{items_html}
  </ul>
  <div class="codex-footer">
    <p>Soli Deo Gloria　·　快樂查經班　·　{book_name}</p>
  </div>
</div>
</div>
</body>
</html>"""


def build_bible_indexes():
    groups = group_bible_files()
    if not groups:
        return EMPTY_NOTE

    os.makedirs("bible", exist_ok=True)
    book_items = []

    for prefix, files in sorted(groups.items()):
        book_name = BOOK_MAP.get(prefix, prefix)
        page_filename = f"{prefix}.html"
        page_path = os.path.join("bible", page_filename)

        page_html = generate_book_page(prefix, files, book_name)
        with open(page_path, "w", encoding="utf-8") as f:
            f.write(page_html)

        chapter_count = len(files)
        book_items.append(
            f'    <li class="article-item">'
            f'<a href="bible/{page_filename}">'
            f'{book_name}'
            f'<span style="margin-left:auto;font-size:0.8rem;opacity:0.5">{chapter_count} 章</span>'
            f'</a></li>'
        )
        print(f"  ✅ {book_name}（{chapter_count} 章）→ {page_path}")

    return "\n".join(book_items)


def build_flat_list(folder):
    if not os.path.isdir(folder):
        return EMPTY_NOTE
    files = sorted([f for f in os.listdir(folder) if f.endswith(".html")])
    if not files:
        return EMPTY_NOTE
    items = []
    for filename in files:
        title = get_title(os.path.join(folder, filename))
        items.append(f'    <li class="article-item"><a href="{folder}/{filename}">{title}</a></li>')
    return "\n".join(items)


def update_index(index_path="index.html"):
    print("📖 掃描 bible/ 書目...")
    bible_html = build_bible_indexes()

    with open(index_path, encoding="utf-8") as f:
        content = f.read()

    pattern = r'(<ul class="article-list" id="list-bible">).*?(</ul>)'
    content = re.sub(pattern, rf'\1\n{bible_html}\n  \2', content, flags=re.DOTALL)

    for folder, list_id in [("groups", "list-groups"), ("devotion", "list-devotion"), ("media", "list-media")]:
        items_html = build_flat_list(folder)
        pattern = rf'(<ul class="article-list" id="{list_id}">).*?(</ul>)'
        content = re.sub(pattern, rf'\1\n{items_html}\n  \2', content, flags=re.DOTALL)

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(content)

    print("✅ index.html 已更新")


if __name__ == "__main__":
    update_index()
