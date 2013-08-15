from pupa.scrape import Jurisdiction

from .people import GrandePrairieCountyNo1PersonScraper
from utils import lxmlize

class GrandePrairieCountyNo1(Jurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/csd:4819006/council'
  geographic_code = 4819006
  def get_metadata(self):
    return {
      'name': 'Grande Prairie County No. 1',
      'legislature_name': 'Grande Prairie County No. 1 City Council',
      'legislature_url': 'http://cms.burlington.ca/Page110.aspx',
      'terms': [{
        'name': 'N/A',
        'sessions': ['N/A'],
      }],
      'provides': ['people'],
      'session_details': {
        'N/A': {
          '_scraped_name': 'N/A',
        }
      },
    }

  def get_scraper(self, term, session, scraper_type):
    if scraper_type == 'people':
        return GrandePrairieCountyNo1PersonScraper

  def scrape_session_list(self):
    return ['N/A']
    