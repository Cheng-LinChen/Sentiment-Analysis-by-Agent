import subprocess
import shutil
import os
import sys

from config import BIT_NEWS_DIR, SOURCE_DIR, REPORT_DIR, SA_DIR, user

def run_bit_news_collection():
    print("Running BIT news collection...")
    if(user == 0):
        subprocess.run([sys.executable, BIT_NEWS_DIR], check=True)
    else:
        subprocess.run(["python", BIT_NEWS_DIR], check=True)
    print("BIT news collection complete.")


def run_sentiment_analysis():
    print("Running sentiment analysis...")
    if(user == 0):
        subprocess.run([sys.executable, BIT_NEWS_DIR], check=True)
    else:
        subprocess.run(["python", SA_DIR], check=True)
    print("Sentiment analysis complete.")

if __name__ == "__main__":
    run_bit_news_collection()
    run_sentiment_analysis()


