import pandas as pd
from pathlib import Path
import copy
from preprocess import preprocess as pp
from nltk.corpus import stopwords


class DataHandler:
    def __init__(self, raw_data_path, processed_data_path, start_date):
        self.start_date = start_date
        self.raw_data_path = raw_data_path
        self.processed_data_path = processed_data_path
        self.raw_dataframe = self.load_historical_raw_dataframe()
        self.processed_dataframe = self.preprocess_data(
            copy.deepcopy(self.raw_dataframe)
        )
        self.processed_dataframe.to_csv(processed_data_path)

    def load_historical_raw_dataframe(self):
        return pd.read_excel(Path(f"{self.raw_data_path}"))

    def preprocess_data(self, data_frame):
        pp.convert_datetime_format(data_frame, "tweetDate", "Date")
        data_frame["text"] = data_frame["text"].apply(pp.remove_stop_words)
        data_frame["text"] = data_frame["text"].apply(pp.remove_hashtags)
        data_frame["text"] = data_frame["text"].apply(pp.remove_english_letters)
        data_frame["text"] = data_frame["text"].apply(pp.remove_non_hebrew)
        data_frame["text"] = data_frame["text"].apply(
            pp.remove_unconventional_punctuation
        )
        data_frame["text"] = data_frame["text"].apply(pp.remove_url)
        data_frame["text"] = data_frame["text"].apply(pp.remove_username)
        data_frame["text"] = data_frame["text"].apply(pp.strip_text)
        data_frame = pp.remove_empty_tweets(data_frame, "text")
        data_frame = data_frame[(data_frame["Date"] > self.start_date.date())]
        data_frame.sort_values(by='Date',inplace=True)
        return data_frame

    def save_processed_data(self, df, filename):
        df.to_csv(filename)

    def load(self, filename):
        return pd.read_csv(filename).drop(columns=["Unnamed: 0"])
