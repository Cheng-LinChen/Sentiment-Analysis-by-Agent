# import time
# import requests
# import csv
# from datetime import datetime, timedelta
# from bs4 import BeautifulSoup
# from googlesearch import search


# # Function to fetch Google search results
# def fetch_google_results(query, num_results=10):
#     links = []
#     for url in search(query, num_results=num_results):
#         links.append(url)
#     return links


# # Function to fetch page content
# def fetch_page_content(url):
#     try:
#         response = requests.get(url, timeout=10)
#         if response.status_code == 200:
#             return response.text
#         return None
#     except requests.exceptions.RequestException as e:
#         print(f"Error fetching {url}: {e}")
#         return None


# # Function to extract title, content, and last modified date
# def extract_content(page_html, url):
#     soup = BeautifulSoup(page_html, "html.parser")
#     title = soup.title.string if soup.title else "No Title"

#     # Extract content
#     paragraphs = soup.find_all("p")
#     content = " ".join([para.get_text() for para in paragraphs])

#     # Extract last modified date from headers
#     last_update = None
#     try:
#         response = requests.head(url, timeout=10)
#         if "Last-Modified" in response.headers:
#             last_update = response.headers["Last-Modified"]
#             last_update = datetime.strptime(
#                 last_update, "%a, %d %b %Y %H:%M:%S %Z"
#             ).strftime("%Y-%m-%d")
#     except requests.exceptions.RequestException:
#         pass

#     return title, content, last_update


# # Function to get Reddit mentions for a domain in the past N days
# def get_reddit_mentions(domain, days_before):
#     url = f"https://www.reddit.com/search.json?q={domain}&sort=new&t={days_before}d"
#     headers = {"User-Agent": "Mozilla/5.0"}
#     try:
#         response = requests.get(url, headers=headers, timeout=10)
#         if response.status_code == 200:
#             data = response.json()
#             return len(data["data"]["children"])  # Count of mentions
#     except Exception as e:
#         print(f"Error fetching Reddit data: {e}")
#     return 0  # Return 0 if request fails


# # Function to save results to CSV
# def save_to_csv(data, filename="search_results_filtered.csv"):
#     with open(filename, mode="w", newline="", encoding="utf-8") as file:
#         writer = csv.writer(file)
#         writer.writerow(["URL", "Title", "Content", "Last Update", "Popularity Score"])
#         for row in data:
#             writer.writerow(row)


# # Main function to fetch, rank, and save search results
# def get_sources(query, result_num, days_before):
#     # Calculate date range
#     start_date = (datetime.now() - timedelta(days=days_before)).strftime("%Y-%m-%d")
#     today_date = datetime.now().strftime("%Y-%m-%d")

#     print(f"Fetching articles from {start_date} to {today_date}...")

#     links = fetch_google_results(query, result_num)

#     extracted_data = []

#     for link in links:
#         print(f"Fetching {link}...")
#         page_html = fetch_page_content(link)
#         if page_html:
#             title, content, last_update = extract_content(page_html, link)
#             domain = link.split("/")[2]  # Extract domain from URL
#             popularity = get_reddit_mentions(domain, days_before)  # Get mentions

#             # Check if last update is within the past N days
#             if last_update and start_date <= last_update <= today_date:
#                 extracted_data.append([link, title, content, last_update, popularity])

#     # Sort data by popularity score (highest first)
#     extracted_data.sort(key=lambda x: x[4], reverse=True)

#     # Save sorted data to CSV
#     if extracted_data:
#         save_to_csv(extracted_data)
#         print(f"Results saved to 'search_results_filtered.csv'")
#     else:
#         print(f"No results found from {start_date} to {today_date}")


# # Run the function
# if __name__ == "__main__":
#     user_query = "TSMC"
#     result_num = 50
#     days_before = 3  # Fetch articles from the last 3 days
#     get_sources(user_query, result_num, days_before)


import time
import requests
import csv
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from googlesearch import search


# Function to fetch Google search results with better filtering
def fetch_google_results(query, num_results=10):
    filtered_query = (
        f"{query} (news OR forum OR discussion OR blog OR comments OR twitter OR reddit)"
        f" -site:wikipedia.org -site:forbes.com -site:investopedia.com"
        f" -site:bloomberg.com -site:reuters.com -site:bbc.com -site:cnn.com -site:nytimes.com"
    )
    links = []
    for url in search(filtered_query, num_results=num_results):
        links.append(url)
    return links


# Function to fetch page content
def fetch_page_content(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.text
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None


# Function to extract title, content, and last modified date
def extract_content(page_html, url):
    soup = BeautifulSoup(page_html, "html.parser")
    title = soup.title.string if soup.title else "No Title"

    # Extract content
    paragraphs = soup.find_all("p")
    content = " ".join([para.get_text() for para in paragraphs])

    # Extract last modified date from headers
    last_update = None
    try:
        response = requests.head(url, timeout=10)
        if "Last-Modified" in response.headers:
            last_update = response.headers["Last-Modified"]
            last_update = datetime.strptime(
                last_update, "%a, %d %b %Y %H:%M:%S %Z"
            ).strftime("%Y-%m-%d")
    except requests.exceptions.RequestException:
        pass

    return title, content, last_update


# Function to get Reddit mentions for a domain in the past N days
def get_reddit_mentions(domain, days_before):
    url = f"https://www.reddit.com/search.json?q={domain}&sort=new&t={days_before}d"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return len(data["data"]["children"])  # Count of mentions
    except Exception as e:
        print(f"Error fetching Reddit data: {e}")
    return 0  # Return 0 if request fails


# Function to save results to CSV
def save_to_csv(data, filename="filtered_news_discussions.csv"):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["URL", "Title", "Content", "Last Update", "Popularity Score"])
        for row in data:
            writer.writerow(row)


# Main function to fetch, rank, and save search results
def get_sources(query, result_num, days_before):
    # Calculate date range
    start_date = (datetime.now() - timedelta(days=days_before)).strftime("%Y-%m-%d")
    today_date = datetime.now().strftime("%Y-%m-%d")

    print(f"Fetching news & discussions from {start_date} to {today_date}...")

    links = fetch_google_results(query, result_num)

    extracted_data = []

    for link in links:
        print(f"Fetching {link}...")
        page_html = fetch_page_content(link)
        if page_html:
            title, content, last_update = extract_content(page_html, link)
            domain = link.split("/")[2]  # Extract domain from URL
            popularity = get_reddit_mentions(domain, days_before)  # Get mentions

            # Check if last update is within the past N days
            if last_update and start_date <= last_update <= today_date:
                extracted_data.append([link, title, content, last_update, popularity])

    # Sort data by popularity score (highest first)
    extracted_data.sort(key=lambda x: x[4], reverse=True)

    # Save sorted data to CSV
    if extracted_data:
        save_to_csv(extracted_data)
        print(f"Results saved to 'filtered_news_discussions.csv'")
    else:
        print(f"No results found from {start_date} to {today_date}")


# Run the function
if __name__ == "__main__":
    user_query = "Bitcoin, War, Tariff, Finaince, Stock, Risk, Trump"
    result_num = 500
    days_before = 3  # Fetch articles from the last 3 days
    get_sources(user_query, result_num, days_before)
