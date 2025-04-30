import subprocess
import shutil
import os

from config import BIT_NEWS_DIR, SOURCE_DIR, REPORT_DIR, SA_DIR

def run_bit_news_collection():
    print("Running BIT news collection...")
    subprocess.run(["python", BIT_NEWS_DIR], check=True)
    print("BIT news collection complete.")

def prepare_sa_input():
    source_file = SOURCE_DIR
    target_folder = REPORT_DIR
    os.makedirs(target_folder, exist_ok=True)
    target_file = os.path.join(target_folder, os.path.basename(source_file))
    shutil.copy(source_file, target_file)
    print(f"Copied {source_file} to {target_file}")

def run_sentiment_analysis():
    print("Running sentiment analysis...")
    subprocess.run(["python", SA_DIR], check=True)
    print("Sentiment analysis complete.")

if __name__ == "__main__":
    run_bit_news_collection()
    prepare_sa_input()
    run_sentiment_analysis()


