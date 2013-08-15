from pupa.scrape import Jurisdiction

from .people import DorvalPersonScraper
from utils import lxmlize

class Dorval(Jurisdiction):
  jurisdiction_id = 'ca-qc-dorval'
  geographic_code = 2466087
  def get_metadata(self):
    return {
      'name': 'Dorval',
      'legislature_name': 'Dorval Municipal Council',
      'legislature_url': 'http://www.ville.dorval.qc.ca/en/default.asp?contentID=516',
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
        return DorvalPersonScraper

  def scrape_session_list(self):
    return ['N/A']
    