import subprocess
import shutil
import os

def run_bit_news_collection():
    print("Running BIT news collection...")
    subprocess.run(["python", r"C:/Users/User/Desktop/專題/Sentiment-Analysis-by-Agent/data collection/BIT.py"], check=True)
    print("BIT news collection complete.")

def prepare_sa_input():
    source_file = r"C:/Users/User/Desktop/專題/Sentiment-Analysis-by-Agent/data collection/finnhub_bit_news_recent.csv"
    target_folder = r"C:/Users/User/Desktop/專題/Sentiment-Analysis-by-Agent/sentiment analysis/source"
    os.makedirs(target_folder, exist_ok=True)
    target_file = os.path.join(target_folder, os.path.basename(source_file))
    shutil.copy(source_file, target_file)
    print(f"Copied {source_file} to {target_file}")

def run_sentiment_analysis():
    print("Running sentiment analysis...")
    subprocess.run(["python", r"C:/Users/User/Desktop/專題/Sentiment-Analysis-by-Agent/sentiment analysis/sa.py"], check=True)
    print("Sentiment analysis complete.")

if __name__ == "__main__":
    run_bit_news_collection()
    prepare_sa_input()
    run_sentiment_analysis()


