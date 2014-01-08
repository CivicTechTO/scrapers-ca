from ca_qc_montreal import MontrealPersonScraper
from utils import CanadianJurisdiction


class Anjou(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/csd:2466023/arrondissement:anjou/council'
  ocd_division = 'ocd-division/country:ca/csd:2466023/arrondissement:anjou'

  def _get_metadata(self):
    return {
      'division_name': 'Anjou',
      'name': u"Conseil d'arrondissement d'Anjou",
      'url': 'http://ville.montreal.qc.ca/anjou',
      'provides': ['people'],
    }

  def get_scraper(self, term, session, scraper_type):
    if scraper_type == 'people':
        return MontrealPersonScraper
