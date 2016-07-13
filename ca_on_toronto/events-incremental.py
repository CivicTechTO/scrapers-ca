from ca_on_toronto.events import TorontoEventScraper
import datetime


class TorontoIncrementalEventScraper(TorontoEventScraper):
    #start_date = datetime.datetime.today() - datetime.timedelta(days=6)
    start_date = datetime.datetime(2016, 6, 7)
    end_date = datetime.datetime(2016, 6, 8)

