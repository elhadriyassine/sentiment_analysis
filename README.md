# Financial News Sentiment Analyzer
This Python script is designed to analyze the sentiment of recent financial news headlines for a user-specified stock ticker. Script can retrieve news for the last seven days.By leveraging the Finnhub API to fetch news data and the NLTK VADER lexicon for sentiment analysis, the script provides a quick overview of public sentiment surrounding a company.

Features
  - Stock Ticker Input: Prompts the user to enter a stock symbol (e.g., AAPL, TSLA).
  - Automated News Fetching: Retrieves news headlines for the last seven days using the Finnhub API.
  - Sentiment Analysis: Analyzes the sentiment of each headline, categorizing it as Positive, Negative, or Neutral.
  - Sentiment Distribution: Calculates and displays the percentage of positive, negative, and neutral headlines.
  - Top Headlines: Identifies and displays the top 10 most positive and top 10 most negative headlines based on their sentiment score.
  - Detailed Results: Provides a complete, scrollable table of all processed articles, including their date, headline, sentiment label, and compound sentiment score.

Requirements
The script has the following dependencies, which will be automatically installed if not found:

nltk: A powerful natural language toolkit for Python.

finnhub: The Python client for the Finnhub API.

pandas: A data manipulation and analysis library, used here for creating and displaying the news data table.

Additionally, a Finnhub API key is required. The script is specifically configured to retrieve this key from Google Colab Secrets. You must store your key in the secrets panel under the name finhubAPI.

How to Run
Set up your Finnhub API Key

In your Google Colab notebook, click on the Key icon in the left sidebar to open the "Secrets" panel.

Click on "+ New secret" and create a new secret with the following details:

Name: finhubAPI

Value: Your Finnhub API key (e.g., abcdefg123456...)

Ensure the checkbox "Notebook access" is enabled for this secret.

Install Libraries:

The script will automatically check for and download the vader_lexicon from NLTK.

You may need to manually install the finnhub-python and pandas libraries if they are not pre-installed in your environment. You can do this by running the following commands in a code cell:

!pip install finnhub-python
!pip install pandas

Execute the Script:

Run the Python code. The script will prompt you to enter a stock ticker symbol.

Expected Output
Upon running the script, you will be prompted to enter a stock symbol. The console output will then follow this sequence:

A confirmation that the Finnhub API key has been retrieved.
A message indicating that news is being fetched for your chosen stock symbol for the last 7 days.
The Sentiment Distribution showing the percentage of positive, negative, and neutral articles.
The Top 10 Most Positive Headlines in a table format.
The Top 10 Most Negative Headlines in a table format.
The All Financial News Sentiment Analysis Results showing a comprehensive table of all headlines processed.
