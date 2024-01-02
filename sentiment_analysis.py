
# This file will take data from main.py and perform simple calculations for sentiment analysis on Twitter data


# Function used to read keywords along with their score from a file
def read_keywords(keyword_file_name):
    keywords = {}
    try:
        with open(keyword_file_name, 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split('\t')
                if len(parts) == 2:
                    keyword, score = parts
                    keywords[keyword] = int(score)

# If file could not be opened an exception is raised 
    except IOError:
        print(f"Could not open file {keyword_file_name}!")
        return {}
    return keywords

# Funcion used to clean tweet text by removing numbers and characters which are not in the alphabet and converting them into lowercase 
def clean_tweet_text(tweet_text):
    cleaned_text = ''.join(char.lower() if char.isalpha() or char.isspace() else '' for char in tweet_text)
    return cleaned_text

# Function used to read the tweets from the file and extracts relevant information such as user, text, favourite, retweet, language, country, city, latitude, longitude, date
def read_tweets(tweet_file_name):
    tweet_list = []
    try:
        with open(tweet_file_name, 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split(',')
                if len(parts) >= 11:
                    lat = float(parts[9]) if parts[9] != 'NULL' else 'NULL'
                    lon = float(parts[10]) if parts[10] != 'NULL' else 'NULL'
                    
                    tweet = {
                        'user': parts[2],  
                        'text': clean_tweet_text(parts[1]),  
                        'favorite': int(parts[4]),
                        'retweet': int(parts[3]),
                        'lang': parts[5],  
                        'country': parts[6],
                        'state': parts[7],  
                        'city': parts[8],  
                        'lat': lat,  
                        'lon': lon,  
                        'date': parts[0]  
                    }
                    tweet_list.append(tweet)

# If file could not be opened an exception is raised 
    except IOError:
        print(f"Could not open file {tweet_file_name}")
        return []
    
# If latitude or longitude values are not valid an exception is raised 
    except ValueError:
        print("Error: Latitude and/or longitude values are not valid.")
        return []
    return tweet_list

# Function uses keywords from the tweet to calculate a sentiment score 
def calc_sentiment(tweet_text, keyword_dict):
    words = tweet_text.split()
    sentiment_score = sum(keyword_dict.get(word, 0) for word in words)
    return sentiment_score

# Function used to classify the sentiment based on the score calculated 
def classify(score):
    if score > 0:
        return "positive"
    elif score < 0:
        return "negative"
    else:
        return "neutral"

# Function used to generate a report based on tweet sentiment and other statistics 
def make_report(tweet_list, keyword_dict):
    num_tweets = len(tweet_list)
    num_positive = sum(1 for tweet in tweet_list if classify(calc_sentiment(tweet['text'], keyword_dict)) == 'positive')
    num_negative = sum(1 for tweet in tweet_list if classify(calc_sentiment(tweet['text'], keyword_dict)) == 'negative')
    num_neutral = sum(1 for tweet in tweet_list if classify(calc_sentiment(tweet['text'], keyword_dict)) == 'neutral')
    num_favorite = sum(1 for tweet in tweet_list if int(tweet['favorite']) > 0)
    num_retweet = sum(1 for tweet in tweet_list if int(tweet['retweet']) > 0)

# Calculate the average sentiment of all the tweets 
    try:
        avg_sentiment = round(sum(calc_sentiment(tweet['text'], keyword_dict) for tweet in tweet_list) / num_tweets, 2)
    # Raise an exception to handel the case where there an no tweets to avoid division by zero 
    except ZeroDivisionError: 
        avg_sentiment = "NAN"
# Calculate the average sentiment of favourited tweets 
    try:
        avg_favorite = round(sum(calc_sentiment(tweet['text'], keyword_dict) for tweet in tweet_list if int(tweet['favorite']) > 0) / num_favorite, 2)
    # Raise an exception to handel the case where there an no favorurited tweets to avoid division by zero 
    except ZeroDivisionError:
        avg_favorite = "NAN"
# Calculate average sentiment of retweeted tweets
    try:
        avg_retweet = round(sum(calc_sentiment(tweet['text'], keyword_dict) for tweet in tweet_list if int(tweet['retweet']) > 0) / num_retweet, 2)
    # Raise an exception to handel the case where there are no retweeted tweets to avoid division by zero
    except ZeroDivisionError:
        avg_retweet = "NAN"

# Calculate average sentiment of each country 
    country_sentiments = {}
    for tweet in tweet_list:
        country = tweet['country']
        if country != 'NULL':
            if country not in country_sentiments:
                country_sentiments[country] = [calc_sentiment(tweet['text'], keyword_dict)]
            else:
                country_sentiments[country].append(calc_sentiment(tweet['text'], keyword_dict))
    avg_country_sentiments = {country: round(sum(scores) / len(scores), 2) for country, scores in country_sentiments.items()}

# Find the top 5 countries by average sentiment 
    top_5_countries = ', '.join(sorted(avg_country_sentiments.keys(), key=lambda x: avg_country_sentiments[x], reverse=True)[:5])

    # Create the final report dictionary 
    report = {
        'avg_sentiment': avg_sentiment,
        'num_tweets': num_tweets,
        'num_positive': num_positive,
        'num_negative': num_negative,
        'num_neutral': num_neutral,
        'num_favorite': num_favorite,
        'avg_favorite': avg_favorite,
        'num_retweet': num_retweet,
        'avg_retweet': avg_retweet,
        'top_five': top_5_countries
    }

    return report

# Function used to write the report to a file
def write_report(report, output_file):

    # Open file in write mode 
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            # Write stastics that were calculated to the file 
            file.write(f"Average sentiment of all tweets: {report['avg_sentiment']}\n")
            file.write(f"Total number of tweets: {report['num_tweets']}\n")
            file.write(f"Number of positive tweets: {report['num_positive']}\n")
            file.write(f"Number of negative tweets: {report['num_negative']}\n")
            file.write(f"Number of neutral tweets: {report['num_neutral']}\n")
            file.write(f"Number of favorited tweets: {report['num_favorite']}\n")
            file.write(f"Average sentiment of favorited tweets: {report['avg_favorite']}\n")
            file.write(f"Number of retweeted tweets: {report['num_retweet']}\n")
            file.write(f"Average sentiment of retweeted tweets: {report['avg_retweet']}\n")
            file.write(f"Top five countries by average sentiment: {report['top_five']}\n")
        # If the file writing is successful print message 
        print(f"Wrote report to {output_file}")
    except IOError:
        # If an exception is rasied an error occurs print error message 
        print(f"Could not open file {output_file}")