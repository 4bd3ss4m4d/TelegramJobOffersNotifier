import os
import time
import re
from jobofferewebsite1_scraper import JobOffersWebsite1Scraper
from telegram_notifier import TelegramNotifier

PREVIOUS_TITLE_TXT_PATH = 'data/previous_titles.txt'
CURRENT_TITLE_TXT_PATH = 'data/current_titles.txt'
WAITING_TIME_BEFORE_EACH_MONITORING = 60 * 60


class JobOffersNotifier:
    # JobOffersNotifier Instance attributes
    def __init__(self):
        self.first_run = False
        self.previous_articles = self._read_previous_articles()
        self.djma_scraper = JobOffersWebsite1Scraper()
        self.new_article_titles = ''
        self.keep_monitoring = True

    # Read previously stored articles private method
    def _read_previous_articles(self):
        # Try to open the text file that contains the previous article titles
        try:
            with open('data/previous_titles.txt', 'r', encoding='utf-8') as infile:
                # Read previously saved files, convert them to lines and start from the 2nd element (1st element is
                # empty)
                previous_articles = infile.read().split('\n')[1:]

            self.first_run = False
            return previous_articles
        # Except if the File is not found
        except FileNotFoundError:
            self.first_run = True
            return None

    # Monitor newly added articles in JobOffersWebsite1 Method
    def monitor(self):

        # extract Titles of the first page
        scraped_articles = self.djma_scraper.scrap_offers(1)

        # Append scraped articles' titles to a new text file named 'current_titles.txt'
        for article in scraped_articles:

            # Write to the txt file
            with open('data/current_titles.txt', 'a', encoding='utf-8') as infile:
                infile.write(f"{article['Job Title']}".rstrip('\n'))
            # if it's the first run , then also create previous articles text file
            if self.first_run:
                with open('data/previous_titles.txt', 'a', encoding='utf-8') as infile:
                    infile.write(f"{article['Job Title']}".rstrip('\n'))

        # Read the new text file created
        with open('data/current_titles.txt', 'r', encoding='utf-8') as infile:
            current_articles = infile.read().split('\n')[1:]

        # Read the previous articles saved
        self.previous_articles = self._read_previous_articles()

        # If current articles' titles equal to the previous article's titles
        if current_articles == self.previous_articles:
            print('No new articles published so far.')

            # Delete the new text file
            if os.path.isfile(CURRENT_TITLE_TXT_PATH):
                os.remove(CURRENT_TITLE_TXT_PATH)

            return None

        else:
            print('New articles have been published!')

            # Split the text file to a list of lines and convert them to a set
            curr_articles_set = set(current_articles)

            prev_articles_set = set(self.previous_articles)

            # Isolate the items that are in the current titles text file and not tht previous one
            new_article_titles = curr_articles_set.difference(prev_articles_set)

            print(f'New published articles are: {new_article_titles}')

            # Assign the new articles to the instance attributes
            self.new_article_titles = list(new_article_titles)

            # Delete the previously saved file text
            if os.path.isfile(PREVIOUS_TITLE_TXT_PATH):
                os.remove(PREVIOUS_TITLE_TXT_PATH)
                print(f"Old previous_titles.txt file has been deleted.")

            # Modify the current text file to 'previous text file'
            if os.path.isfile(CURRENT_TITLE_TXT_PATH):
                os.rename(CURRENT_TITLE_TXT_PATH, PREVIOUS_TITLE_TXT_PATH)
                print(f"Modify the current text file to 'previous text file'.")

            articles_to_publish = []

            # Loop through scraped articles
            for article in scraped_articles:

                # Delete the \n from article titles
                article_title = re.sub('\n', '', article['Job Title'])

                # Loop through each new article
                for new_article in self.new_article_titles:

                    # Check if it's a match
                    if new_article == article_title:
                        articles_to_publish.append(article)

            return articles_to_publish

