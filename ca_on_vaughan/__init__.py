from utils import CanadianJurisdiction, lxmlize

import re

class Vaughan(CanadianJurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/csd:3519028/council'
  geographic_code = 3519028
  def _get_metadata(self):
    return {
      'name': 'Vaughan',
      'legislature_name': 'Vaughan City Council',
      'legislature_url': 'http://www.vaughan.ca/council/Pages/default.aspx',
      'terms': [{
        'name': '2010-2014',
        'sessions': ['2010-2014'],
        'start_year': 2010,
        'end_year': 2014,
      }],
      'session_details': {
        '2010-2014': {
          '_scraped_name': '2010-2014',
        }
      },
    }
  def scrape_session_list(self):
    page = lxmlize('http://www.vaughan.ca/council/Pages/default.aspx')
    session = page.xpath('//*[@id="WebPartTitleWPQ2"]/h3/span[1]')[0].text_content()
    session = re.findall(r'[0-9]{4}-[0-9]{4}', session)[0]
    return [str(session)]
