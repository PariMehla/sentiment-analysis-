
# This file uses the module to analyze Twitter information. 

# Import functions from sentiment_analysis file 
from sentiment_analysis import read_keywords, read_tweets, make_report, write_report

def main():
   
    # Get user input for filenames
    keyword_filename = input("Input keyword filename (.tsv file): ")
    # Check to see if the filename has the right extension 
    if not keyword_filename.endswith(".tsv"):
        raise Exception("Invalid keywords file! Must have tsv file extension!")
    # Get user input for tweet filename 
    tweet_filename = input("Input tweet filename (.csv file): ")
    # Check to see if the filename has the right extension 
    if not tweet_filename.endswith(".csv"):
        raise Exception("Invalid tweets file! Must have csv file extension!")
    # Get user input for report filename 
    report_filename = input("Input filename to output report in (.txt file): ")

    # Check to see file extensions
    if not report_filename.endswith(".txt"):
        raise Exception("Invalid report file! Must have txt file extension!")
    # Check to see if the tweet file is valid
    if not tweet_filename or not tweet_filename.strip():
        raise Exception("Invalid tweets file! Please provide a valid filename.")
    # Check to see if the tweet file exists
    try:
        with open(tweet_filename, 'r') as tweet_file:
            # Check to see if the file is empty
            if tweet_file.readline() == "":
                raise Exception("Tweets file is empty!")
    # Raise an exception if the file is not found 
    except FileNotFoundError:
        raise Exception("Tweets file not found!")
    # Read keyword and tweet data
    keyword_dict = read_keywords(keyword_filename)
    # Read tweet data and check to see if the tweet list is empty
    tweet_list = read_tweets(tweet_filename)
    if not tweet_list:
        raise Exception("Tweets file is empty!")
    # Check to see if keyword dictionary is empty
    if not keyword_dict:
        raise Exception("Keyword dictionary is empty!")
    # Check to see if the tweet dictionary is empty
    if not tweet_list:
        raise Exception("Tweet dictionary is empty!")
    # Create report
    report = make_report(tweet_list, keyword_dict)
    # Write report to file
    write_report(report, report_filename)
    

if __name__ == "__main__":
    main()