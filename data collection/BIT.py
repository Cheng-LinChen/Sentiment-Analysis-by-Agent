import finnhub
import pandas as pd
from datetime import datetime, timedelta

# 初始化 Finnhub 客戶端
api_key = "cv418thr01ql2euu1ahgcv418thr01ql2euu1ai0"  # 你的 API 金鑰
finnhub_client = finnhub.Client(api_key=api_key)

# 計算過去7天的時間範圍
seven_days_ago = datetime.now() - timedelta(days=7)
seven_days_ago_timestamp = int(seven_days_ago.timestamp())  # 轉換為 UNIX 時間戳

# 獲取新聞數據
try:
    all_news = finnhub_client.general_news('crypto', min_id=0)  # 獲取加密貨幣相關新聞

    # 檢查數據是否有效
    if all_news:
        # 篩選包含 "bitcoin"、"crypto"、"blockchain" 等關鍵字的新聞
        bit_news = [
            news for news in all_news 
            if ("bitcoin" in news['headline'].lower() or "crypto" in news['headline'].lower() or "blockchain" in news['headline'].lower()) and 
               news['datetime'] >= seven_days_ago_timestamp
        ]

        if bit_news:
            # 轉換為 DataFrame
            df = pd.DataFrame(bit_news)

            # 選擇關鍵欄位
            df = df[['datetime', 'headline', 'source', 'summary', 'url']]

            # 將 datetime 轉換為可讀格式
            df['datetime'] = pd.to_datetime(df['datetime'], unit='s')

            # 儲存成 CSV
            df.to_csv("finnhub_bit_news_recent.csv", index=False, encoding="utf-8-sig")

            print(f"Success! Saved {len(bit_news)} BIT related news from the past 7 days.")
        else:
            print("No BIT related news from the past 7 days found.")
    else:
        print("No news available.")
except Exception as e:
    print(f"Error: {e}")

