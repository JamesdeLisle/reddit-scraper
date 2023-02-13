from time import sleep

from reddit_scraper.scraper import Scraper
from reddit_scraper.time_keeper import TimeKeeper 

timekeeper = TimeKeeper()

scraper = Scraper()
scraper.scrape('coronavirus', 1)
while True:
    if timekeeper.is_tomorrow():
        scraper.scrape('coronavirus', 1)
    sleep(60)