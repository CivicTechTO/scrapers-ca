from ca_qc_montreal import MontrealPersonScraper
from utils import CanadianJurisdiction


class LeSudOuest(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/csd:2466023/arrondissement:le_sud-ouest/council'
  ocd_division = 'ocd-division/country:ca/csd:2466023/arrondissement:le_sud-ouest'

  def _get_metadata(self):
    return {
      'name': 'Le Sud-Ouest',
      'legislature_name': u"Conseil d'arrondissement du Sud-Ouest",
      'legislature_url': 'http://ville.montreal.qc.ca/sud-ouest',
      'provides': ['people'],
    }

  def get_scraper(self, term, session, scraper_type):
    if scraper_type == 'people':
        return MontrealPersonScraper
