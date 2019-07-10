import requests
import logging
import json


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

def log_call(f):
    def wrapper(*args, **kwargs):
        logger.info('Calling {}...'.format(f.__name__))
        f(*args, **kwargs)
    return f



class WarframeMarketItemApi():
    def __init__(self, item_name):
        self.item_name = item_name

        
    @log_call
    def _sanitize_name(self):
        if self.item_name.split(' ')[-1] == 'Prime':
            self.item_name += ' Set'
        _sanitized_name = self.item_name.replace(' ', '_').replace('&', '_and_').lower()
        logger.info('Sanitized name is {}'.format(_sanitized_name))
        return _sanitized_name

    @log_call
    def get_statistics(self):
        headers = {
            'Content-type': 'application/json'
        }
        url = 'https://api.warframe.market/v1/items/{}/statistics'.format(self._sanitize_name())
        
        r = requests.get(url, headers=headers)
        try:
            self.last_2_days_stats = json.loads(r.text)['payload']['statistics_closed']['48hours']
        except:
            print(r.text)

        for item in self.last_2_days_stats:
            print('{} - Min price: {} - Max price: {} - Average: {}'.format(item['datetime'], item['min_price'], item['max_price'], item['avg_price']))


a = WarframeMarketItemApi('Mesa Prime')

a.get_statistics()