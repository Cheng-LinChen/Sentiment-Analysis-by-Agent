import finnhub
import pandas as pd

# 初始化 Finnhub 客戶端
api_key = "cv418thr01ql2euu1ahgcv418thr01ql2euu1ai0"  # 替換為你的 API 金鑰
finnhub_client = finnhub.Client(api_key=api_key)

# 設定要獲取的新聞數量
news_limit = 100  # 修改此數字來獲取不同數量的新聞

# 獲取新聞數據
try:
    news = finnhub_client.general_news('general', min_id=0)

    # 檢查數據是否有效
    if news:
        # 只取前 news_limit 筆新聞
        news = news[:news_limit]

        # 轉換為 DataFrame
        df = pd.DataFrame(news)

        # 選擇關鍵欄位
        df = df[['datetime', 'headline', 'source', 'summary', 'url']]

        # 將 datetime 轉換為可讀格式
        df['datetime'] = pd.to_datetime(df['datetime'], unit='s')

        # 儲存成 CSV
        df.to_csv("finnhub_news_limited.csv", index=False, encoding="utf-8-sig")

        print(f"success finnhub_news_limited.csv（x {news_limit} ）")
    else:
        print("no news")
except Exception as e:
    print(f"error: {e}")