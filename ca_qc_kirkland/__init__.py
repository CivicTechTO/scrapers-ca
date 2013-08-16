from utils import CanadianJurisdiction

class Kirkland(CanadianJurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/csd:2466102/council'
  geographic_code = 2466102
  def _get_metadata(self):
    return {
      'name': 'Kirkland',
      'legislature_name': 'Kirkland City Council',
      'legislature_url': 'http://www.ville.kirkland.qc.ca/portrait-municipal/conseil-municipal/elus-municipaux',
    }
