from transformers import AutoModelForSequenceClassification
from transformers import AutoTokenizer, AutoConfig
from scipy.special import softmax
import os
import pandas as pd
from preprocess import preprocess as pp


class SentimentModel:
    def __init__(self, model_name):
        self.model_name = model_name
        # Check if tokenizer already exists, otherwise create it
        tokenizer_saved_path = "cardiffnlp/tokenizer"
        if os.path.exists(tokenizer_saved_path):
            self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_saved_path)
        else:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.tokenizer.save_pretrained(tokenizer_saved_path)
        self.config = AutoConfig.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)

    def score(self, text):
        encoded_input = self.tokenizer(text, return_tensors="pt")
        output = self.model(**encoded_input)
        scores = output[0][0].detach().numpy()
        scores = softmax(scores)
        return scores

    def score_from_tweets_df(self, df):
        # Create a new DataFrame to store the average sentiment score for each date
        sentiment_df = pd.DataFrame(
            columns=[
                "Date",
                "Text",
                "Negative_Score",
                "Natural_Score",
                "Positive_Score",
            ]
        )

        # Iterate over each date and calculate the average sentiment score for all tweets on that date
        for tweet in df.iterrows():
            text = tweet[1].text
            date = tweet[1].Date
            sentiment_score = self.score(text)
            new_row = pd.DataFrame(
                {
                    "Date": date,
                    "Text": text,
                    "Negative_Score": sentiment_score[0],
                    "Natural_Score": sentiment_score[1],
                    "Positive_Score": sentiment_score[2],
                },
                index=[0],
            )
            sentiment_df = pd.concat([sentiment_df, new_row], ignore_index=True)

        sentiment_df = pp.calculate_avarge_rolling(sentiment_df,'Negative_Score',250)
        return sentiment_df
    

