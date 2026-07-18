#
# 需要先安裝 python 套件: torch, transfomers 
# 測試在以下套件版本執行成功
#   torch: 2.11.0+cpu
#   transformers: 5.12.1
#   ckip_transformers: 0.3.4
# 
# 安裝指令:
#   pip torch==2.11.0 --index-url https://download.pytorch.org/whl/cpu 
#   pip transformers==5.12.1
#   pip ckip_transformers==0.3.4
#


import os
import time
import pandas as pd
from ckip_transformers.nlp import CkipWordSegmenter



# 1. 載入新聞標題
news_title_fname = "tsmc_news_2026_back.csv"
news_title_df = pd.read_csv(news_title_fname)
news_title_list = news_title_df["title"].tolist()
print(f"news_title_list: {news_title_list}")
news_num = len(news_title_list)


# 2. 載入 CKIP Transformers (bert-chinese) 模型
ws_model_fpath = f"models/ckip_bert_chinese_ws"

# 如果模型沒有儲存在local，會從hugging face下載模型
if not os.path.exists(ws_model_fpath):
    os.makedirs(ws_model_fpath)
    ws_driver  = CkipWordSegmenter(model="bert-base")

    # 儲存模型在local，避免超過hugging face的下載次數
    ws_driver.tokenizer.save_pretrained(ws_model_fpath)
    ws_driver.model.save_pretrained(ws_model_fpath)
else:
    ws_driver  = CkipWordSegmenter(model_name=ws_model_fpath)


# 3. 載入斷詞結果，如果沒有，會進行斷詞
news_ws_fname = "tsmc_news_2026_ckip_bert_ws_1.json"
if os.path.exists(news_ws_fname):
    news_ws_df = pd.read_json(news_ws_fname)
    news_ws_list = news_ws_df["token"].tolist()
    print(f"載入斷詞結果: {news_ws_fname}")
else:
    # run pipeline
    # it may take a while...
    # need save results to file to avoid rerun it

    print(f"使用 CKIP BERT-Chinese 斷詞...")
    st = time.time()
    news_ws_list = ws_driver(news_title_list)
#    print("ws_driver:")
#    print(ws_driver(news_title_list))
    et = time.time()
    print(f"CKIP BERT-Chinese 花費: {et - st:.3f} 秒")

    #for i in range(news_num):
    #    print(news_title_list[i])
    #    print(news_ws_list[i])
    #    print()

    # 儲存 CKIP Transformers 斷詞結果
    # transform list to DataFrame
    news_token_df = pd.DataFrame({"token": news_ws_list})
    # save dataframe to JSON file
    news_token_df.to_json(news_ws_fname, orient="records")


# 4. 載入 NTUSD 正向/負向詞
pos_fpath = "NTUSD/正面詞無重複_9365詞.txt"
neg_fpath = "NTUSD/負面詞無重複_11230詞.txt"

pos_df = pd.read_csv(pos_fpath, header=None, names=["word"], encoding="big5")
pos_words_list = pos_df["word"].tolist()
#print(pos_words_list)

neg_df = pd.read_csv(neg_fpath, header=None, names=["word"], encoding="big5")
neg_words_list = neg_df["word"].tolist()
#print(neg_words_list)


# 5. 製作新聞字典 (包含 斷詞結果 和 情緒字典)
news_dicts_list = []
for i in range(news_num):
    news_dict = {}

    title = news_title_list[i]
    tokens_list = news_ws_list[i]

    # make NTUSD sentiment dict
    sent_dict = {"pos": {}, "neg": {},
                 "pos_cnt": 0, "neg_cnt": 0,
                 "score": 0, "label": ""}

    for token in tokens_list:
        if token in pos_words_list:
            sent_dict["pos_cnt"] += 1

            if token in sent_dict["pos"]:
                sent_dict["pos"][token] += 1
            else:
                sent_dict["pos"][token] = 1

        if token in neg_words_list:
            sent_dict["neg_cnt"] += 1

            if token in sent_dict["neg"]:
                sent_dict["neg"][token] += 1
            else:
                sent_dict["neg"][token] = 1

    # compute score
    sent_dict["score"] = sent_dict["pos_cnt"] - sent_dict["neg_cnt"]

    # label based on socre
    if sent_dict["score"] > 0:
        sent_dict["label"] = "正面"
    elif sent_dict["score"] == 0:
        sent_dict["label"] = "中立"
    else:
        sent_dict["label"] = "負面"

    # record tokens and sentiment dict
    news_dict["tokens"] = tokens_list
    news_dict["sent_dict"] = sent_dict
    news_dicts_list.append(news_dict)

# 6. 檢查 斷詞 和 情緒字典 的結果
for news_dict in news_dicts_list:
    print(news_dict["tokens"])
    print(news_dict["sent_dict"])
    print()


# 7. 儲存結果為一份 JSON 檔
news_dict_fname = "tsmc_news_2026_ckip_bert_tokens_n_sents_1.json"
news_dict_df = pd.DataFrame(news_dicts_list)
news_dict_df.to_json(news_dict_fname, orient="records")


# 8. 載入 JSON 檔，確認儲存和載入的資料一樣
news_dict_df2 = pd.read_json(news_dict_fname)

print(f"news_dict_df and news_dict_df2 are equal: {news_dict_df.equals(news_dict_df2)}")

