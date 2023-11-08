import streamlit as st
import os
import seaborn as sns
import pandas as pd

from model import sentiment_model as sm
from pages import pages_builder as pb 
from data import data_handler as dh
from configuration import config as cf

# Set Seaborn theme to "dark"
sns.set_theme(style="dark")
st.set_page_config(layout="wide")


# Streamlit app
def streamlit_app_builder(sentiment_scores_df):
    _,c2,_=st.columns([0.5, 1, 0.5])
    with c2:
        # Streamlit configuration
        st.title(":blue[Israel Political Twitter Sentiment Analysis]")

    # Sidebar selection
    st.sidebar.title("Analysis Options")
    st.sidebar.write("Choose a type of analysis:")
    option = st.sidebar.radio("", ["WordCloud Analysis", "Time Series Analysis", "Tabular & Histogram Analysis"])

    # Main content based on selection
    st.sidebar.write("---")
    if option == "WordCloud Analysis":
        st.sidebar.write("You selected: WordCloud Analysis")
        pb.create_wordcloud_page(sentiment_scores_df, st)
    elif option == "Time Series Analysis":
        st.sidebar.write("You selected: Time Series Analysis")
        pb.create_time_series_page(sentiment_scores_df, st)
    elif option == "Tabular & Histogram Analysis":
        st.sidebar.write("You selected: Tabular & Histogram Analysis")
        pb.create_tabular_histogram_page(sentiment_scores_df, st)


if __name__ == "__main__":
    # Load the YAML configuration file
    cfg = cf.set_config()

    # Load configurations 
    model_name = cfg.model_params.model_name
    raw_data_path = cfg.data_paths.raw_data_path
    processed_data_path = cfg.data_paths.processed_data_path
    start_date_time = pd.to_datetime(cfg.data_filters.start_date_time)
    output_path = cfg.data_paths.output_path

    # Initialize the sentiment model
    sentiment_model = sm.SentimentModel(model_name)

    # Initialize the data handler
    data_handler = dh.DataHandler(raw_data_path, processed_data_path, start_date_time)

    # Check if the output file already exists
    if os.path.exists(output_path):
        print("Loading sentiment scores from existing file...")
        sentiment_scores_df = data_handler.load(output_path)
    else:
        print("Calculating sentiment scores and saving to the output file...")
        sentiment_scores_df = sentiment_model.score_from_tweets_df(
            data_handler.processed_dataframe
        )
        try:
            data_handler.save_processed_data(sentiment_scores_df, output_path)
            print("Sentiment scores saved successfully.")
        except Exception as e:
            print(f"Error saving sentiment scores: {str(e)}")

    #Running the streamlit builder     
    try:
        streamlit_app_builder(sentiment_scores_df)
        print("Sentiment scores saved successfully.")
    except Exception as e:
        print(f"Error while running streamlit app: {str(e)}")
