from wordcloud import WordCloud
from bidi.algorithm import get_display
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.models import DatetimeTickFormatter
import pandas as pd


def generate_word_cloud(text, color):
    if color == "RED":
        wordcloud = WordCloud(
            color_func=red_color_func,
            width=300,
            height=300,
            background_color="white",
            max_words=200,
            min_font_size=10,
            font_path="davidbd.ttf",
        ).generate(text)
    elif color == "GREEN":
        wordcloud = WordCloud(
            color_func=green_color_func,
            width=300,
            height=300,
            background_color="white",
            max_words=200,
            min_font_size=10,
            font_path="davidbd.ttf",
        ).generate(text)
    elif color == "BLUE":
        wordcloud = WordCloud(
            color_func=blue_color_func,
            width=300,
            height=300,
            background_color="white",
            max_words=200,
            min_font_size=10,
            font_path="davidbd.ttf",
        ).generate(text)
    else:
            wordcloud = WordCloud(
            width=300,
            height=300,
            background_color="white",
            max_words=200,
            min_font_size=10,
            font_path="davidbd.ttf",
        ).generate(text)
    return wordcloud


def build_word_cloud_tweet(df, color):
    bidi_text = list()
    for i, r in df.iterrows():
        bidi = convert_bidi_text(r["Text"])
        bidi_text.append(bidi)
    wordcloud = generate_word_cloud("".join(bidi), color)
    return wordcloud


def convert_bidi_text(text):
    bidi_text = ""
    if isinstance(text, str):
        try:
            bidi_text = get_display(text)
        except:
            print(f"Can't Convert the follown text : {str}", text)
            bidi_text = ""
    return bidi_text


def green_color_func(
    word, font_size, position, orientation, random_state=None, **kwargs
):
    return "hsl(120, 100%, 50%)"  # Green colo


def red_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    return "hsl(0, 100%, 50%)"  # Red color


def blue_color_func(
    word, font_size, position, orientation, random_state=None, **kwargs
):
    return "hsl(210, 100%, 50%)"  # Blue color

def plot_twittes_by_time(df, column_name, upper_th, lower_th):
    df['Date'] = pd.to_datetime(df['Date'])
    df.sort_values(by='Date',inplace=True)
    df["AreaSentiment"] = [
        "red" if score > upper_th else "yellow" if score > lower_th else "green"
        for score in df[column_name]
    ]

    # Create a ColumnDataSource from the DataFrame
    source = ColumnDataSource(df)
    # Create the figure
    p = figure(
        title="Twitters Avarage Sentiment Scores  Over Time",
        x_axis_label="Date",
        y_axis_label=column_name,
    )

    # Add a scatter plot
    p.scatter("Date", column_name, source=source, color="AreaSentiment")

    # Format the x-axis tick labels
    p.xaxis[0].formatter = DatetimeTickFormatter(months="%Y-%m-%d %H:%M:%S")

    # Add hover tool to display the text when hovering over a data point
    hover = HoverTool(
        tooltips=[("Text", "@Text"), ("Date", "@Date{%F}")],
        formatters={"@Date": "datetime"},
    )
    p.add_tools(hover)
    # Show the plot
    return p
