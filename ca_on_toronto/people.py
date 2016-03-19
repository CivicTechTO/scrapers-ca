from __future__ import unicode_literals
from utils import CSVScraper

COUNCIL_PAGE = 'http://www1.toronto.ca/wps/portal/contentonly?vgnextoid=c3a83293dc3ef310VgnVCM10000071d60f89RCRD'


class TorontoPersonScraper(CSVScraper):
    csv_url = 'http://www1.toronto.ca/City%20Of%20Toronto/Information%20&%20Technology/Open%20Data/Data%20Sets/Assets/Files/Toronto_Elected_Officials.csv'
    district_name = '{district name} ({district id})'
    other_names = {
        'Norman Kelly': ['Norm Kelly'],
        'Justin Di Ciano': ['Justin J. Di Ciano'],
    }

    def scrape(self):
        for p in super(TorontoPersonScraper, self).scrape():
            # Mayor has an odd relative link redirect
            # TODO: Fix lxmlize in utils.py to deal with this
            if p._related[0].role == 'Councillor':
                person_page_url = p.sources[1]['url']
                page = self.lxmlize(person_page_url)
                appointments = page.xpath("//aside//section[contains(.//h2, 'appointments')]//li/a")
                for a in appointments:
                    org_name = a.text_content().strip()
                    p.add_membership(org_name)

            yield p

