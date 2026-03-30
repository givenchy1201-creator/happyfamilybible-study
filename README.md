# 快樂查經班 · Happy Family Bible Study

查經章節、小組討論、靈修手冊、影片資源的線上集合。

## 資料夾結構

```
happyfamilybible-study/
├── index.html          ← 首頁（自動生成，不要手動編輯）
├── build_index.py      ← 自動更新首頁的腳本
├── .github/
│   └── workflows/
│       └── build-index.yml  ← GitHub Action
├── bible/              ← 查經章節
├── groups/             ← 小組討論
├── devotion/           ← 靈修手冊
└── media/              ← 影片資源
```

## 新增文章的方法

1. 把寫好的 HTML 檔案上傳到對應的資料夾（例如查經放 `bible/`）
2. 上傳後 GitHub Action 自動執行，約 1 分鐘內首頁會自動更新
3. Netlify 偵測到更新，約 30 秒後網站上線

## 注意事項

- `index.html` 由程式自動維護，請不要手動編輯它
- 每個 HTML 檔案的 `<title>` 標籤內容會成為首頁顯示的文章標題
- 檔案名稱建議使用英文加底線，例如 `mark_chapter1.html`

---

Soli Deo Gloria
