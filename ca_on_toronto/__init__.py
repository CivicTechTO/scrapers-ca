from __future__ import unicode_literals
from .jurisdiction import TorontoJurisdiction

import lxml.html
import requests


class Toronto(TorontoJurisdiction):
    classification = 'legislature'
    division_id = 'ocd-division/country:ca/csd:3520005'
    division_name = 'Toronto'
    name = 'Toronto City Council'
    url = 'http://www.toronto.ca'
    legislative_sessions = []

    def __init__(self):
        super(Toronto, self).__init__()
        # TODO: Accommodate legacy format pages. (bad old PDF days)
        # {'identifier': '1998-2000'},
        # {'identifier': '2000-2003'},
        # {'identifier': '2003-2006'},
        self.legislative_sessions = [self.build_leg_session(term) for term in self.fetch_tmmis_terms()]

    def get_session_list(self):
        return [term['label'] for term in self.fetch_tmmis_terms()]

    def build_leg_session(self, term):
        leg_session = {}
        start_year, end_year = term['label'].split('-')
        leg_session['identifier'] = term['label']
        leg_session['name'] = term['label']
        leg_session['start_date'] = '{}-12-01'.format(start_year)
        leg_session['end_date'] = '{}-11-30'.format(end_year)
        leg_session['classification'] = 'primary'

        return leg_session

    def fetch_tmmis_terms(self):
        response = requests.get('http://app.toronto.ca/tmmis/findAgendaItem.do?function=doPrepare')
        page = lxml.html.fromstring(response.text)
        # Remove the blank option label and sort chronologically
        for option in reversed(page.xpath('//select[@name="termId"][1]/option')[1:]):
            term = {}
            term['id'] = option.attrib['value']
            term['label'] = option.text
            yield term

    def current_leg_session(self):
        return self.legislative_sessions[-1]
