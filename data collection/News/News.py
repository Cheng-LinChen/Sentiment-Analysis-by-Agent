import requests
import pandas as pd
from datetime import datetime, timedelta

# from newsapi import NewsApiClient

api_key = "4ea2c375a3ec4af8b5bd8cb50819ba36"  # Replace with your actual API key
query = "TSMC"  # Query for TSMC-related news

# Calculate the date range for the last three days
end_date = datetime.now()
start_date = end_date - timedelta(days=1)

# Format the dates in the required 'YYYY-MM-DD' format
from_date = start_date.strftime("%Y-%m-%d")
to_date = end_date.strftime("%Y-%m-%d")

# Construct the URL with the query, date range, and pageSize parameter to limit the number of results to 50
url = f"https://newsapi.org/v2/everything?q={query}&apiKey={api_key}&pageSize=100&from={from_date}"

# Fetch the news data
response = requests.get(url)
data = response.json()


# api = NewsApiClient(api_key="XXXXXXXXXXXXXXXXXXXXXXX")
# Check if the request was successful
if response.status_code == 200:
    articles = data["articles"]
    news_data = []

    for article in articles:
        # Fetch content or article body (Note: Some articles might not have full content)
        content = article.get("content", "No content available")

        # Get source information (from the article's source)
        source_name = article["source"]["name"]

        news_data.append(
            {
                "Title": article["title"],
                "Description": article["description"],
                "Content": content,  # Adding content field
                "URL": article["url"],
                "PublishedAt": article["publishedAt"],
                "Source": source_name,
            }
        )

    # Sort the news data by source
    df = pd.DataFrame(news_data)
    df_sorted = df.sort_values(by="Source")  # Sorting by Source name

    # Save to CSV
    df_sorted.to_csv("tsmc_news_last_3_days_sorted.csv", index=False)
    print(
        "TSMC news from the last 3 days with content, sorted by source, saved to 'tsmc_news_last_3_days_sorted.csv'"
    )
else:
    print(f"Failed to fetch news: {data['message']}")
