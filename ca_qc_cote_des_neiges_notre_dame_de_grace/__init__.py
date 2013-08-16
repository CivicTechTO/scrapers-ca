from ca_qc_montreal import MontrealPersonScraper
from utils import CanadianJurisdiction

class Cote_des_Neiges_Notre_Dame_de_Grace(CanadianJurisdiction):
  jurisdiction_id = 'ca-qc-cote-des-neiges-notre-dame-de-grace'

  def _get_metadata(self):
    return {
      'name': 'Cote-des-Neiges-Notre-Dame-de-Grace',
      'legislature_name': 'Cote-des-Neiges-Notre-Dame-de-Grace Borough Council',
      'legislature_url': 'http://depot.ville.montreal.qc.ca/bd-elus/data.json',
      'provides': ['people'],
    }

  def get_scraper(self, term, session, scraper_type):
    if scraper_type == 'people':
        return MontrealPersonScraper
