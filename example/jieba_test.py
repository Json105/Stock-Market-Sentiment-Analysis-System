import jieba  #pip3 install jieba
import pandas as pd

df = pd.read_csv("TaiwanStockNews_test.csv")
for title in df["title"]:
  #text = "金融新聞情緒分析"
  words = jieba.lcut_for_search(title)

  print(words)

