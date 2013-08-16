from utils import CanadianJurisdiction

class CapeBreton(CanadianJurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/csd:1217030/council'
  geographic_code = 1217030
  def _get_metadata(self):
    return {
      'name': 'Cape Breton',
      'legislature_name': 'Cape Breton City Council',
      'legislature_url': 'http://www.cbrm.ns.ca/councillors.html',
    }
