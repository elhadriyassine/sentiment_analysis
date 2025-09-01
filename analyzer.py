from google.colab import userdata
from IPython.display import display 
import finnhub
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
import datetime
import time



#  Download NLTK VADER Lexicon 
try:
    nltk.data.find('sentiment/vader_lexicon')
except LookupError:
    print("Downloading NLTK vader_lexicon...")
    nltk.download('vader_lexicon')
    print("Download complete.")

#  Initialize Sentiment Analyzer
analyzer = SentimentIntensityAnalyzer()

#  Retrieve Finnhub API Key from Colab Secrets 
try:
    finnhub_api_key = userdata.get('finhubAPI')
    if not finnhub_api_key:
         raise ValueError("Finnhub API key not found in Colab Secrets.")
    print("Successfully retrieved Finnhub API key.")
except Exception as e:
    print(f"Error retrieving API key from Colab Secrets: {e}")
    print("Please make sure you have stored your Finnhub API key in Colab Secrets under the name 'finhubAPI'.")
    
    exit()

#  Initialize Finnhub Client 
try:
    finnhub_client = finnhub.Client(api_key=finnhub_api_key)
    print("Finnhub client initialized.")
except Exception as e:
    print(f"Error initializing Finnhub client: {e}")
    exit() 

#  Get Stock Symbol from User 
stock_symbol = input("Please enter the stock ticker symbol (e.g., AAPL, TSLA, NVDA): ").strip().upper()

if not stock_symbol:
     print("No symbol entered. Exiting.")
     exit()

#  Define Date Range (Last 7 days) 
# Get today's date
today = datetime.date.today()
# Calculate the date 7 days ago
one_week_ago = today - datetime.timedelta(days=7)

# Format dates for the Finnhub API (YYYY-MM-DD)
from_date_str = one_week_ago.strftime('%Y-%m-%d')
to_date_str = today.strftime('%Y-%m-%d')

print(f"Fetching news for {stock_symbol} from {from_date_str} to {to_date_str}...")

#  Fetch Company News 
try:
    # Use the company_news endpoint which takes symbol and date range
    news_data = finnhub_client.company_news(
        symbol=stock_symbol,
        _from=from_date_str,
        to=to_date_str
    )
    print(f"Fetched {len(news_data)} articles for {stock_symbol}.")

    if not news_data:
        print(f"No news found for {stock_symbol} in the past week.")

except finnhub.exceptions.FinnhubAPIException as e:
    print(f"Finnhub API error fetching news for {stock_symbol}: {e}")
    print("Please check the symbol, your API key, and rate limits.")
    news_data = [] 
except Exception as e:
    print(f"An unexpected error occurred while fetching news for {stock_symbol}: {e}")
    news_data = [] 


#  Perform Sentiment Analysis and Prepare Data 
articles_data = []

if news_data:
    print("Analyzing sentiment for headlines...")
    for article in news_data:
        # Check if required keys exist
        title = article.get('headline')
        timestamp = article.get('datetime') 

        if title and timestamp is not None:
            try:
                
                article_datetime = datetime.datetime.fromtimestamp(timestamp)
                date_str = article_datetime.strftime('%Y-%m-%d %H:%M:%S') 

                # Perform sentiment analysis on the headline
                sentiment_scores = analyzer.polarity_scores(title)

                # VADER's compound score is a normalized score (-1 to +1)
                compound_score = sentiment_scores['compound'] # Store the raw compound score

                # Determine the sentiment label based on the compound score
                sentiment_label = 'Neutral'
                if compound_score >= 0.05:
                    sentiment_label = 'Positive'
                elif compound_score <= -0.05:
                    sentiment_label = 'Negative'

                articles_data.append({
                    'Date': date_str,
                    'Title': title,
                    'Sentiment': sentiment_label,
                    'Compound_Score': compound_score # Add the compound score to the data
                })

            except (TypeError, ValueError) as e:
                print(f"Could not process timestamp {timestamp} or analyze title: {e}. Skipping article.")
            except Exception as e:
                 print(f"An unexpected error occurred processing article: {e}. Skipping.")
        else:
             # This handles cases where 'headline' or 'datetime' might be missing
             # print(f"Skipping an article due to missing title or datetime: {article}") # Uncomment for debugging
             pass # Silently skip articles with missing data

    print(f"Successfully processed {len(articles_data)} articles for sentiment.")

else:
    print("No news data available to process sentiment.")


#  Create Pandas DataFrame 
sentiment_df = pd.DataFrame(articles_data)

# Convert 'Date' column to datetime objects for proper sorting
if not sentiment_df.empty:
    sentiment_df['Date'] = pd.to_datetime(sentiment_df['Date'])
    # Optional: Sort the main DataFrame by date
    sentiment_df = sentiment_df.sort_values(by='Date').reset_index(drop=True)

#  Function to Calculate Sentiment Percentages 

def analyze_sentiment_percentages(sentiment_df):

    sentiment_percentages = {}

    # Check if the DataFrame is valid and has the 'Sentiment' column
    if sentiment_df is None or sentiment_df.empty or 'Sentiment' not in sentiment_df.columns:
        print("DataFrame is empty or missing 'Sentiment' column. Cannot calculate percentages.")
        return sentiment_percentages

    # Get the counts for each sentiment label
    sentiment_counts = sentiment_df['Sentiment'].value_counts()

    # Calculate the total number of articles
    total_articles = len(sentiment_df)

    if total_articles > 0:
        # Calculate the percentage for each label
        for label, count in sentiment_counts.items():
            percentage = (count / total_articles) * 100
            sentiment_percentages[label] = round(percentage, 2) # Round to 2 decimal places

    return sentiment_percentages

#  How to use the function (Add this after the DataFrame is created in your previous script) 

# Assuming sentiment_df has been created successfully from the previous steps

if 'sentiment_df' in locals() and not sentiment_df.empty:
    # Call the function to get percentages
    sentiment_results = analyze_sentiment_percentages(sentiment_df)

    # Print the results
    print("\n Sentiment Distribution ")
    if sentiment_results:
        for label, percentage in sentiment_results.items():
            print(f"{label}: {percentage}%")
    else:
        print("Could not calculate sentiment distribution.")

else:
    print("\nNo sentiment DataFrame available to calculate percentages.")


#  Display Top/Bottom Sentiment Headlines 
if not sentiment_df.empty:

  # Filter for  top 10 positive sentiment and sort by compound score descending
    print("\n Top 10 Most Positive Headlines ")
    positive_news = sentiment_df[sentiment_df['Sentiment'] == 'Positive'].sort_values(
        by='Compound_Score', ascending=False
    ).head(10) 

    if not positive_news.empty:
        # Display only relevant columns for the summary
        display(positive_news[['Date', 'Title', 'Sentiment', 'Compound_Score']])
    else:
        print("No positive headlines found.")

  # Filter for negative sentiment and sort by compound score ascending
    print("\n Top 10 Most Negative Headlines ")
    negative_news = sentiment_df[sentiment_df['Sentiment'] == 'Negative'].sort_values(
        by='Compound_Score', ascending=True
    ).head(10) 

    if not negative_news.empty:
         # Display only relevant columns for the summary
        display(negative_news[['Date', 'Title', 'Sentiment', 'Compound_Score']])
    else:
        print("No negative headlines found.")
else:
     print("\nNo news data to display top/bottom sentiments.")


#  Display Full Financial News Sentiment Analysis Results (Scrollable) 
if not sentiment_df.empty:
    print("\n All Financial News Sentiment Analysis Results ")
    pd.set_option('display.width', 1460)
    # pd.set_option('display.max_colwidth', None)
    pd.set_option('display.max_rows', None) 
    pd.set_option('display.max_columns', None)
    # pd.set_option('display.width', None) # Uncomment to prevent wrapping

    display(sentiment_df[['Date', 'Title', 'Sentiment', 'Compound_Score']]) 
else:
    print("\nNo full sentiment analysis results to display.")
