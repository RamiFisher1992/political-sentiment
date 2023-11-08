
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import pandas as pd
from visual import utilits as viz_util

# Function to create WordCloud
def create_wordcloud_page(df, st):
    #Create Container
    container1 = st.container()
    # Display tweet's word cloud
    container1.subheader("Tweet's Word Cloud")
    # User input for search query
    search_query = container1.text_input("Filtered only tweets with filtered word :","דמוקרטיה")
    # Filter the DataFrame based on user input
    c1, c2, c3 = st.columns([1, 1, 1])
    if search_query:
        with c1:
            st.write(":blue[Full Filtered Tweet's Word Cloud ]")
            filtered_df = df[
                df["Text"].str.contains(search_query, case=False, na=False)
            ]
            overall_word_cloud = viz_util.build_word_cloud_tweet(filtered_df,"")
            plt.figure(figsize=(10, 5))
            plt.imshow(overall_word_cloud, interpolation="bilinear")
            plt.axis("off")
            st.pyplot(plt)
        top_n_twittes = st.slider(
            "Top N Ranked Twittes:",
            1,
            int(len(filtered_df)),
            int(len(filtered_df) / 5),
        )
        with c2:
            # Top x Postive twittes
            st.write(":green[Top #N Positve Tweet's Word Cloud ]")
            top_positive_tweets = filtered_df.sort_values(
                by="Positive_Score", ascending=False
            ).head(top_n_twittes)
            word_cloud = viz_util.build_word_cloud_tweet(top_positive_tweets, "GREEN")
            plt.figure(figsize=(10, 5))
            plt.imshow(word_cloud, interpolation="bilinear")
            plt.axis("off")
            st.pyplot(plt)
        with c3:
            # Top x Negative twittes
            st.write(":red[Top #N Negative Tweet's Word Cloud ]")
            top_negative_tweets = filtered_df.sort_values(
                by="Negative_Score", ascending=False
            ).head(top_n_twittes)
            word_cloud = viz_util.build_word_cloud_tweet(top_negative_tweets, "RED")
            plt.figure(figsize=(10, 5))
            plt.imshow(word_cloud, interpolation="bilinear")
            plt.axis("off")
            st.pyplot(plt)
    else:
        st.write("Enter a search query to get results.")


# Function to create Temporal Chart
def create_time_series_page(df, st):
    _, c2, _ = st.columns([1, 6, 1])
    with c2:
        upper_thresh = st.slider(
            label = "Upper Threshold:",
            step = 0.01,
            min_value = df['Negative_Score_Rolling'].mean(),
            max_value =max(df['Negative_Score_Rolling']),
            value = float(max(df['Negative_Score_Rolling'])-df['Negative_Score_Rolling'].mean())/2 + df['Negative_Score_Rolling'].mean()
        )
        lower_thresh = st.slider(
            label  = "Lower Threshold:",
            step = 0.01,
            min_value = min(df['Negative_Score_Rolling']),
            max_value = df['Negative_Score_Rolling'].mean(),
            value = float(df['Negative_Score_Rolling'].mean()-min(df['Negative_Score_Rolling']))/2 + min(df['Negative_Score_Rolling'])
        )
        tem_plot = viz_util.plot_twittes_by_time(df,'Negative_Score_Rolling',upper_thresh,lower_thresh)
        st.bokeh_chart(tem_plot,use_container_width=True)


# Display sentiment analysis results
def create_tabular_histogram_page(df, st):
    c1, c2, c3 = st.columns([1, 6, 1])

    with c2:
        filtered_df = df
        # Convert the 'Date' column to datetime
        filtered_df["Date"] = pd.to_datetime(filtered_df["Date"])
        # Streamlit configuration
        st.write("### Filtering Tweetes")
        # User input for search query
        search_query = st.text_input("Enter a search query:","דמוקרטיה")
        # Filter the DataFrame based on user input
        if search_query:
            filtered_df = filtered_df[
                filtered_df["Text"].str.contains(search_query, case=False, na=False)
            ]
        else:
            st.write("Enter a search query to get results.")

        # Date filter
        date_range = st.date_input(
            "Select a date range:",
            [filtered_df["Date"].min(), filtered_df["Date"].max()],
        )
        # Convert date_range to datetime objects
        start_date = datetime.combine(date_range[0], datetime.min.time())
        end_date = datetime.combine(date_range[1], datetime.max.time())

        if date_range:
            # Filter the DataFrame based on the selected date range
            filtered_df = filtered_df[
                (filtered_df["Date"] >= start_date) & (filtered_df["Date"] <= end_date)
            ]

        st.write("### Search Results")
        st.dataframe(filtered_df)

        # Streamlit configuration
        st.write("### Filtered Data Histogram")
        options =["Negative_Score", "Positive_Score", "Natural_Score"]
        # User input for column to plot
        columns_to_plot = st.multiselect(
            "Select columns to plot as a histogram:",
            options,default=options
        )
        # Define a dictionary to map column names to colors
        color_mapping = {
            "Negative_Score": "red",
            "Positive_Score": "green",
            "Natural_Score": "yellow",
        }

        # Check if columns are selected
        if columns_to_plot:
            # Create a figure and axis for the plot
            fig, ax = plt.subplots()

            # Plot histograms for selected columns with different colors based on the column name
            for column in columns_to_plot:
                color = color_mapping.get(
                    column, "gray"
                )  # Default to gray if column not in mapping
                sns.histplot(
                    filtered_df[column],
                    bins=10,
                    ax=ax,
                    color=color,
                    label=column,
                    kde=True,
                )  # Use sns.histplot with kde=True

            # Set labels and title
            ax.set_xlabel("Values")
            ax.set_ylabel("Frequency")

            # Add a legend
            ax.legend()

            # Display the plot in Streamlit
            st.pyplot(fig,use_container_width=True)
        else:
            st.write("Select at least one column to plot as a histogram.")
