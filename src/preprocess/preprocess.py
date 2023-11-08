import pandas as pd
import re
from datetime import datetime
from nltk.corpus import stopwords
import nltk


# Convert TweetDate column to datetime format
def convert_datetime_format(df, raw_date_column_name, pp_date_column_name):
    df[raw_date_column_name] = df[raw_date_column_name].apply(
        lambda x: datetime.strptime(x, "%a %b %d %H:%M:%S +0000 %Y")
    )
    df[raw_date_column_name] = pd.to_datetime(
        df[raw_date_column_name], format="%Y-%m-%d %H:%M:%S"
    )
    df[pp_date_column_name] = df[raw_date_column_name].dt.date
    return df


# Function to clean the text by removing URLs
def remove_url(text):
    url_pattern = r"http\S+"
    return re.sub(url_pattern, "", text)


# Function to clean the text by removing Usernames
def remove_username(text):
    username_pattern = r"@\w+"
    return re.sub(username_pattern, "", text)


# Function to clean the text by removing hashtags
def remove_hashtags(text):
    hashtags_pattern = r"#\w+"
    return re.sub(hashtags_pattern, "", text)


# Function to clean the text by removing unconventional punctuation
def remove_unconventional_punctuation(text):
    unconventional_punctuation_pattern = r"[^\w\s]"
    return re.sub(unconventional_punctuation_pattern, "", text)


# Function to clean the text by removing non-Hebrew characters
def remove_non_hebrew(text):
    non_hebrew_pattern = r"[^\u0590-\u05FF\s]+"
    return re.sub(non_hebrew_pattern, "", text)


# Function to clean the text by removing english characters
def remove_english_letters(text):
    english_letters_pattern = r"[a-zA-Z]"
    return re.sub(english_letters_pattern, "", text)


# Function to clean the text by removing whitespace characters
def remove_whitespace_spaces(text):
    whitespace_spaces_pattern = r"\s+"
    return re.sub(whitespace_spaces_pattern, "", text)


# Function to clean the text by Trim leading/trailing whitespace
def strip_text(text):
    text = text.strip()
    return text

    # Function to clean the text by removing URLs and usernames


def remove_stop_words(text):
    try:
        nltk.corpus.stopwords.words("hebrew")
    except LookupError:
        nltk.download("stopwords")

    # Get the Hebrew stopwords
    hebrew_stopwords = set(stopwords.words("hebrew"))
    hebrew_stopwords.add("זו")
    hebrew_stopwords.add("ב")
    hebrew_stopwords.add("ה")
    hebrew_stopwords.add("על")
    hebrew_stopwords.add("לא")

    # Removing standard stop words
    cleaned_text = " ".join(
        [
            word
            for word in nltk.word_tokenize(text)
            if word.lower() not in hebrew_stopwords
        ]
    )
    return cleaned_text


# Remove rows where 'text' column is empty or contains only whitespace
def remove_empty_tweets(df, column_name):
    df = df.dropna(subset=[column_name])
    df = df[df[column_name].str.strip().astype(bool)]
    df = df.reset_index(drop=True)
    return df


def calculate_avarge_rolling(df,column_name,window_size):
    df = df.reset_index(drop=True)
    df[column_name+'_Rolling'] = df[column_name].rolling(window_size,min_periods=window_size).mean()
    df = df.dropna()
    return df
