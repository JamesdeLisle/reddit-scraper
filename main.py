from time import sleep

from reddit_scraper.scraper import Scraper
from reddit_scraper.time_keeper import TimeKeeper 

timekeeper = TimeKeeper()

scraper = Scraper()
scraper.scrape('coronavirus', 365, 100000)
while True:
    sleep(60)
    if timekeeper.is_tomorrow():
        scraper.scrape('coronavirus', 1, 100000)