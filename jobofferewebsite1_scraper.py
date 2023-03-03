# Import libraries
from bs4 import BeautifulSoup
import requests
import re
import time
import os

from requests_headers import HEADERS

# Constants
JOB_OFFERS_WEBSITE1 = os.environ.get("DB_JOB_OFFERS_WEBSITE1")
WAITING_TIME = 1


class JobOffersWebsite1Scraper:
    # Defining instance attributes
    def __init__(self):
        self.jobofferswebsite1_url = JOB_OFFERS_WEBSITE1
        self.headers = HEADERS
        self.jobofferswebsite1_session = requests.Session()
        self.total_page_number = self.get_num_of_pages()
        self.current_page = 0

    # Extract HTML Source code of a page Method
    def get_source_code(self, url):
        # Send an HTTP Get request using Session created
        response = self.jobofferswebsite1_session.get(url=url, headers=self.headers)
        # Get the HTML source code of the response
        html_source_code = response.text

        return html_source_code

    # Get number of pages on JobOffersWebsite1 Method
    def get_num_of_pages(self):
        # Scrap the 1st page to get the total number of pages
        url_to_scrap = f'{self.jobofferswebsite1_url}page/1/'
        # Get the HTML source code
        html_source_code = self.get_source_code(url_to_scrap)
        # Create a BeautifulSoup object
        soup = BeautifulSoup(html_source_code, 'lxml')
        # Get <span> that has info about total page numbers
        total_pages_num_raw = soup.find('span', class_='page_info').get_text()
        # Extract total page numbers
        total_pages_num = int(re.sub(r'(Page 1 de )', '', total_pages_num_raw))

        return total_pages_num

    # Scrap data of a page or pages
    def scrap_offers(self, num_of_pages_to_scrap=1, **kwargs):

        job_offers = []

        # In case of scraping a specific page
        spec_page_to_scrap = kwargs.get('specific_page_to_scrap')

        # If there is a value in spec_page_to_scrap, there will be only 1 loop
        if spec_page_to_scrap is not None:
            num_of_pages_to_scrap = 1

        for i in range(int(num_of_pages_to_scrap)):

            # If we don't want to scrap a specific page
            if spec_page_to_scrap is None:
                # Update current page attribute
                self.current_page = i + 1
            else:
                self.current_page = int(spec_page_to_scrap)

            print(f'Scraping page number {self.current_page}')

            # Set the page number of url to scrap
            url_to_scrap = f'{self.jobofferswebsite1_url}page/{self.current_page}/'

            # Get the HTML source code
            html_source_code = self.get_source_code(url_to_scrap)

            soup = BeautifulSoup(html_source_code, 'lxml')

            # Locate sidebar's <div> element that contains unwanted offers
            sidebar = soup.find('div', class_='jeg_sidebar')

            # Delete sidebar's <div> element from the soup
            sidebar.decompose()

            # Find all <article> elements
            article_elements = soup.find_all('article')

            # Assign the value of the argument 'num_of_offers' if given, else none will be assigned
            num_of_offers = kwargs.get('num_of_offers')

            # If none is assigned to the num of offers, then assign the length of article elements to it
            if num_of_offers is None:
                num_of_offers = len(article_elements)

            counter = 0

            # Loop through all <article> elements
            for article_element in article_elements:

                counter += 1

                if counter <= num_of_offers:
                    job_title_and_link_raw = article_element.find('h3', class_='jeg_post_title')

                    # Job Title
                    job_title = job_title_and_link_raw.text
                    # Job Link
                    job_link = job_title_and_link_raw.find('a')['href']
                    # Date of Publication
                    publishing_date = article_element.find('div', class_='jeg_meta_date').get_text()

                    job_offer_info = {'Job Title': job_title,
                                      'Job Link': job_link,
                                      'Publishing Date': publishing_date}

                    # Append job offer to the Job offers list
                    job_offers.append(job_offer_info)

            # Sleep between each page scraping operation
            time.sleep(WAITING_TIME)

        return job_offers

