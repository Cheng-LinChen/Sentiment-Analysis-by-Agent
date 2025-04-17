import requests
import pandas as pd
from datetime import datetime, timedelta

# Set the API key and endpoint
api_key = "pub_73400b087ee408673780a5ffd1bebee335fa8"
query = "TSMC"

# Get the current date and the date 3 days ago
today = datetime.today()
three_days_ago = today - timedelta(days=3)

# Format dates in YYYY-MM-DD format
from_date = three_days_ago.strftime("%Y-%m-%d")
to_date = today.strftime("%Y-%m-%d")

# Set the URL with the parameters
url = url = f"https://newsdata.io/api/1/latest?apikey={api_key}&q={query}"

# Send the GET request
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()  # Convert the response to JSON

    # Initialize a list to store article details
    articles = []

    # Iterate over the articles in the response
    for article in data.get("results", []):
        articles.append(
            {
                "Title": article.get("title"),
                "Description": article.get("description"),
                "PubDateTimeZone": article.get("pubDateTZ"),
                "Content": article.get("content"),
                "Country": article.get("country"),
                "URL": article.get("source_url"),
                "Source": article.get("creator"),
                "Language": article.get("language"),
            }
        )

        # Stop once we have 10 articles
        if len(articles) >= 100:
            break

    # Save the articles to a DataFrame and then to a CSV
    if articles:
        df = pd.DataFrame(articles)
        df.to_csv("tsmc_news.csv", index=False)
        print(f'Successfully saved {len(articles)} articles to "tsmc_news.csv".')
    else:
        print("No articles found.")
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")
