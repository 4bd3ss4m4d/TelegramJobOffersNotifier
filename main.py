import time

from telegram_notifier import TelegramNotifier
from monitor import JobOffersNotifier

WAITING_TIME_BEFORE_EACH_MONITORING = (60 * 60)


def write_article_to_publish(job_offer_dict):
    article_to_publish = f'''
    \n{job_offer_dict["Job Title"]}\n
    Pour plus d\'informations, cliquer sur le lien suivant: {job_offer_dict["Job Link"]}\n
    L\'annonce a été publiée le {job_offer_dict["Publishing Date"]}.
    '''

    return article_to_publish


def main():
    # Create an instance of JobOffersNotifier Class
    djma_monitor = JobOffersNotifier()

    keep_monitoring = True

    while keep_monitoring:

        new_job_offers = djma_monitor.monitor()

        # If there is new articles
        if new_job_offers is not None:

            articles_to_publish = []

            for new_job_offer in new_job_offers:
                # append after creating article to publish
                articles_to_publish.append(write_article_to_publish(new_job_offer))

            telegram_notifier = TelegramNotifier()

            telegram_notifier.publish(articles_to_publish)

        else:
            print('sleeping for 1h')
            time.sleep(WAITING_TIME_BEFORE_EACH_MONITORING)


if __name__ == '__main__':
    main()
