# import praw
# import pandas as pd
# import time
# import datetime

# # Reddit API credentials (Replace with your own credentials)
# CLIENT_ID = "iIT7Q_qnvXqEfqqvCPOEUA"
# CLIENT_SECRET = "cd8rK_jxw5ObvnJJToap5G6o9eqZHg"
# USER_AGENT = "User-Agent:chrome:sem_analyze:python script:v1.0 (by /u/Foreign_Ad5982)"

# # Initialize PRAW Reddit instance
# reddit = praw.Reddit(
#     client_id=CLIENT_ID,
#     client_secret=CLIENT_SECRET,
#     user_agent=USER_AGENT,
# )


# def get_reddit_posts(subreddit, time_filter="week", limit=100):
#     subreddit = reddit.subreddit(subreddit)
#     posts = []
#     for post in subreddit.top(time_filter=time_filter, limit=limit):
#         posts.append(
#             {
#                 "Title": post.title,
#                 "Text": post.selftext,
#                 "Score": post.score,
#                 "Number of Comments": post.num_comments,
#                 "Created UTC": datetime.datetime.utcfromtimestamp(post.created_utc),
#                 "ID": post.id,
#                 "URL": post.url,
#             }
#         )
#     return posts


# # Example usage
# subreddit_name = "trump"
# posts = get_reddit_posts(subreddit_name)

# # Convert to pandas DataFrame
# df = pd.DataFrame(posts)

# # Save the DataFrame as a CSV file in the current directory
# csv_filename = "reddit_posts.csv"
# df.to_csv(csv_filename, index=False)

# print(f"Collected {len(posts)} posts and saved to {csv_filename}")


import praw
import pandas as pd
import time
import datetime

# Reddit API credentials (Replace with your own credentials)
CLIENT_ID = "iIT7Q_qnvXqEfqqvCPOEUA"
CLIENT_SECRET = "cd8rK_jxw5ObvnJJToap5G6o9eqZHg"
USER_AGENT = "User-Agent:chrome:sem_analyze:python script:v1.0 (by /u/Foreign_Ad5982)"

# Initialize PRAW Reddit instance
reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    user_agent=USER_AGENT,
)


def get_reddit_posts_and_comments(subreddit, time_filter="week", limit=10):
    subreddit = reddit.subreddit(subreddit)
    posts = []
    for post in subreddit.top(time_filter=time_filter, limit=limit):
        # Fetching post details
        post_data = {
            "Title": post.title,
            "Text": post.selftext,
            "Score": post.score,
            "Number of Comments": post.num_comments,
            "Created UTC": datetime.datetime.utcfromtimestamp(post.created_utc),
            "ID": post.id,
            "URL": post.url,
            "Comments": [],  # Initialize empty list for comments
        }

        # Collecting comments for the post
        post.comments.replace_more(limit=0)  # Remove "More Comments" objects
        for comment in post.comments.list():
            post_data["Comments"].append(comment.body)

        posts.append(post_data)
        time.sleep(1)  # Delay to avoid hitting rate limits

    return posts


# Example usage
subreddit_name = "trump"
posts = get_reddit_posts_and_comments(subreddit_name)

# Convert to pandas DataFrame
df = pd.DataFrame(posts)

# Save the DataFrame as a CSV file in the current directory
csv_filename = "reddit_posts_with_comments.csv"
df.to_csv(csv_filename, index=False)

print(f"Collected {len(posts)} posts with comments and saved to {csv_filename}")
