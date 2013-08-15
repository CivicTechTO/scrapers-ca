from pupa.scrape import Jurisdiction

from .people import St_CatharinesPersonScraper
from utils import lxmlize

class St_Catharines(Jurisdiction):
  jurisdiction_id = 'ca-on-st_catharines'
  geographic_code = 3526053
  def get_metadata(self):
    return {
      'name': 'St. Catharines',
      'legislature_name': 'St. Catharines City Council',
      'legislature_url': 'http://www.stcatharines.ca/en/governin/BrianMcMullanMayor.asp',
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
        return St_CatharinesPersonScraper

  def scrape_session_list(self):
    return ['N/A']
    