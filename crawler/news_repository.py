# INSERT資料

from mysql_connection import get_connection

def save_news_to_mysql(df):
    if df.empty:
        return  # 如果爬蟲今天沒有抓到任何新聞，傳進來的 df 是空的，函數會直接結束（return）。

    conn = get_connection()
    cursor = conn.cursor() # 呼叫 get_connection() 取得與 MySQL 的連線（conn），並建立一個游標對象（cursor）來執行 SQL 指令。

    sql = """
    INSERT IGNORE INTO news_raw
    (date, stock_id, link, source, title)
    VALUES (%s, %s, %s, %s, %s)
    """
    # INSERT IGNORE：MySQL 我的表1複合鍵是link+id 發現網址重複時，會自動忽略（跳過） 該筆重複的資料，繼續寫入下一筆，非常適合用來做爬蟲防重刷機制。
    # %s 控制符：這是 SQL 參數化查詢。它能確保不論新聞標題（title）裡包含多少奇怪的符號（如引號 ' 或 "），都不會導致 SQL 語法解析失敗，同時能有效防止 SQL 注入攻擊 (SQL Injection)。

    data = []

    for _, row in df.iterrows():
        data.append((
            row.get("date"),
            row.get("stock_id"),
            row.get("link"),
            row.get("source"),
            row.get("title"),
        ))
    # 使用 .iterrows() 逐行讀取 DataFrame。利用 .get() 安全地取出各個欄位的值，轉換後的 data 會長這樣：[(date1, id1, link1...), (date2, id2, link2...)。

    cursor.executemany(sql, data)
    conn.commit()
    # executemany 會將 data 陣列中的數百、數千筆資料打包成一個大封包，一次性發送給 MySQL，寫入效能會比迴圈寫入提升數十倍。
    # conn.commit()：正式提交事務（Transaction），將剛才批次處理的資料真正寫入儲存。

    print(f"💾 已寫入 {cursor.rowcount} 筆 MySQL")
    # cursor.rowcount：返回受到影響的資料筆數。因為使用了 INSERT IGNORE，這個數字代表的是真正成功寫入的全新新聞筆數（重複被跳過的筆數不會被算進去）。

    cursor.close()
    conn.close()
    # 關閉連線: 釋放資料庫的連線資源，避免資料庫因連線數過多而崩潰