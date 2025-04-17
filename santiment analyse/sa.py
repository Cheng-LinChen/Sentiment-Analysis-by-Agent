import os
import pandas as pd
from openai import OpenAI
import json
from tqdm import tqdm
from datetime import datetime
import ast  # Import ast for safe evaluation
import re

client = OpenAI(
    api_key="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"
)


def universal_file_loader(source_folder):
    """
    Load all files from a folder, supporting multiple file types.
    """
    loaded_contents = []
    files = os.listdir(source_folder)
    for filename in files:
        file_path = os.path.join(source_folder, filename)
        try:
            file_extension = os.path.splitext(filename)[1].lower()
            if file_extension == ".csv":
                df = pd.read_csv(file_path)
            elif file_extension == ".json":
                df = pd.read_json(file_path)
            elif file_extension in [".xlsx", ".xls"]:
                df = pd.read_excel(file_path)
            elif file_extension in [".txt", ".log"]:
                with open(file_path, "r") as f:
                    lines = f.readlines()
                    df = pd.DataFrame({"text": lines})
            else:
                continue
            loaded_contents.append(df)
        except Exception as e:
            print(f"Error loading {filename}: {e}")
    if not loaded_contents:
        raise ValueError("No files could be loaded from the source folder.")
    return pd.concat(loaded_contents, ignore_index=True)


def split_text_into_chunks(text, max_tokens=10000):
    """
    Splits text into chunks of approximately max_tokens tokens.
    """
    words = text.split()
    chunks = []
    current_chunk = []
    current_length = 0

    for word in words:
        current_length += len(word) + 1  # +1 for space
        if current_length > max_tokens:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            current_length = len(word) + 1
        current_chunk.append(word)

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


def parse_sentiment_response(sentiment_text):
    # Remove the square brackets and any extra spaces
    sentiment_text = sentiment_text.strip()[1:-1].strip()

    # Find all numbers (both positive and negative) in the string
    numbers = re.findall(r"-?\d+\.\d+", sentiment_text)

    # Extract the factors (first 4 numbers) and the summary (remaining text after numbers)
    factors = {}
    try:
        if len(numbers) == 4:
            factors["price"] = numbers[0]
            factors["volume"] = numbers[1]
            factors["volatility"] = numbers[2]
            factors["trend"] = numbers[3]
    except:
        print("except\n")
        print("numbers: ", numbers)
        factors["price"] = "0.00"
        factors["volume"] = "0.00"
        factors["volatility"] = "0.00"
        factors["trend"] = "0.00"

    # Extract the summary part (everything after the numbers)
    summary_match = re.search(r"summary: (.+)", sentiment_text)
    summary = summary_match.group(1) if summary_match else ""

    return factors, summary


def query_openai(text, key_word):
    """
    Query OpenAI for sentiment analysis and a brief summary in one request.
    """
    prompt = (
        f"You are a sentiment analysis expert. Below is a collection of news, posts, and comments from websites and social media. "
        f"Based on this information, predict the next trading day's price movement of {key_word}. "
        f"Respond with a list of key metrics and their sentiment scores followed by a brief summary, in the format as: "
        f"['price: <V1>', 'volume: <V2>', 'volatility: <V3>', 'trend: <V4>', 'summary: <Summary>']. "
        f"Where <V1>, <V2>, <V3>, <V4> are sentiment scores you predict for each metric, and each value is a float with 2 decimals. "
        f"The sentiment score should be in the range [-1.00, 1.00], where a positive value means you predict the factor (price, volume, volatility, or trend) will increase, "
        f"and a negative value means you predict the factor will decrease. The absolute value indicates the magnitude. "
        f"The <Summary> should be a brief 150-word summary of the sentiment derived from the content.\n"
        f"Please make sure the list is formatted exactly as shown, and the summary should be concise, not exceeding 150 words.\n"
        f"{text}"
    )

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt},
            ],
        )
        sentiment_text = response.choices[0].message.content.strip()
        sentiment_data = sentiment_text

        return sentiment_data
    except Exception as e:
        print(sentiment_text)
        print(f"OpenAI API error: {e}")
        return []


def query_final_summary(text, key_word):
    """
    Query OpenAI to summarize the primary summaries into a final 300-word summary.
    """
    prompt = (
        f"Below are multiple brief summaries from sentiment analysis of {key_word}. "
        f"Please provide a detailed final summary of these summaries in approximately 500 words.\n\n{text}"
    )
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt},
            ],
        )
        final_summary = response.choices[0].message.content.strip()
        return final_summary
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return ""


def analyze_sentiment(data, key_word):
    """
    Perform sentiment analysis and generate summary in one call for each chunk of data.
    """
    text_columns = [col for col in data.columns if data[col].dtype == "object"]
    if not text_columns:
        raise ValueError("No text column found in the DataFrame")

    # Combine text columns into one column
    combined_text = "\n".join(
        data[text_columns].astype(str).apply(lambda x: " ".join(x), axis=1)
    )

    # Split the combined text into smaller chunks (max_tokens = 10000 for OpenAI model)
    text_chunks = split_text_into_chunks(combined_text, max_tokens=10000)

    sentiment_scores = []
    primary_summaries = []  # List to store primary summaries
    cnt = 1
    for chunk in text_chunks:
        sentiment_data = query_openai(chunk, key_word)
        if sentiment_data:
            # Extract the first four numbers as sentiment scores and the rest as summary
            factors, summary = parse_sentiment_response(sentiment_data)
            print("t4")
            # Extend the sentiment scores and store the summary
            if factors:
                print("t5")
                sentiment_scores.append(
                    [
                        float(factors["price"]),
                        float(factors["volume"]),
                        float(factors["volatility"]),
                        float(factors["trend"]),
                    ]
                )
            else:
                print("t6")
                sentiment_scores.append([0.00, 0.00, 0.00, 0.00])
            print("t7")
            primary_summaries.append(summary)

            print("score: ", sentiment_scores)
            print("summary: ", summary)
            print(f"pass {cnt}\n")
            cnt = cnt + 1
            if cnt >= 50:
                break

    # Combine all primary summaries into one final summary
    summary_concat = " ".join(primary_summaries)
    final_sentiment_summary = query_final_summary(summary_concat, key_word)

    return sentiment_scores, final_sentiment_summary


def main():
    key_word = "Bitcoin"
    source_folder = "./source"
    report_folder = "./report"
    os.makedirs(report_folder, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_path = os.path.join(
        report_folder, f"stock_sentiment_analysis_{timestamp}.csv"
    )
    print("t1")
    try:
        # Load the data from the source folder
        data = universal_file_loader(source_folder)
        print("t2")
        # Analyze sentiment and generate the final summary
        sentiment_scores, final_summary = analyze_sentiment(data, key_word)
        print("t3")
        # Calculate average sentiment score
        avg_score = (
            [sum(col) / len(col) for col in zip(*sentiment_scores)]
            if sentiment_scores
            else [-10.00, -10.00, -10.00, -10.00]
        )

        # Prepare the DataFrame for sentiment scores
        df = pd.DataFrame({"sentiment_analysis": sentiment_scores})

        # Open the CSV file and write the custom headers
        with open(report_path, "w") as f:
            # Write the title and date
            title = f"{key_word} Market Sentiment Analysis Report\n"
            date_line = f"Date,{datetime.now().strftime('%Y-%m-%d')}\n"
            f.write(title)
            f.write(date_line)

            # Define factor names
            factor_names = ["price", "volume", "volatility", "trend"]

            # Write average scores
            f.write("Average Sentiment Scores\n")
            for factor, score in zip(factor_names, avg_score):
                f.write(f"{factor},{score:.4f}\n")
            f.write("\n")

            # Write iteration scores in table format
            f.write("Sentiment Score by Iteration\n")
            header = (
                "factor,"
                + ",".join([f"iter{i+1}" for i in range(len(sentiment_scores))])
                + "\n"
            )
            f.write(header)

            # Transpose sentiment_scores to write rows by factor
            for i, factor in enumerate(factor_names):
                row = (
                    factor
                    + ","
                    + ",".join(
                        [f"{float(scores[i]):.4f}" for scores in sentiment_scores]
                    )
                    + "\n"
                )
                f.write(row)

            # Add the final summary
            f.write("\nFinal Sentiment Summary:\n")
            f.write(final_summary)

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
