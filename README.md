# FinMood/Stock-Market-Sentiment-Analysis-System
python's project
# FinMood/Stock-Market-Sentiment-Analysis-System 
# 股票市場情緒分析系統

> 一句話描述：為 {誰} 解決 {什麼} 問題。

---

## 為什麼做這個

{用 2-3 句話說明：業務痛點是什麼、現況有多痛、你們想做到什麼}

---

## 系統架構
![alt text](image.png)

```
Source → Ingest → Storage → Process → Serve → Observe
```

把上面每個階段換成你們實際用的工具，例如：

| 階段 | 工具 |
|---|---|
| Source | {例：Spotify API / Kaggle CSV / 公開資料} |
| Ingest | Python |
| Storage | MySQL / MongoDB |
| Process | pandas / SQL |
| Serve | FastAPI / Streamlit |
| Observe | LINE Notify / Sentry |

---

## 快速開始

```bash
git clone https://github.com/FinMood/Stock-Market-Sentiment-Analysis-System.git
cd Stock-Market-Sentiment-Analysis-System
cp .env.example .env   # 填入需要的 API keys
pip install -r requirements.txt
python main.py
```

---

## 團隊
分工
Table 1 —> Table 3 : 2~3位(包含斷詞等處理)
Table 3+ Table 2 —> Table 4  ： 2~3位  (包含建立API)

| 成員 | 負責範圍 | GitHub |
|---|---|---|
| 王翠賢 | {負責什麼} | @[user1](https://github.com/Cuei-Sian/portfolio) |
| {Name} | {負責什麼} | @user2 |
| {Name} | {負責什麼} | @user3 |

---

## 進度追蹤

見 [task.md](task.md)

---

## License

MIT
