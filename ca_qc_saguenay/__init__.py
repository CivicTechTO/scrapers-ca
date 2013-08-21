from utils import CanadianJurisdiction


class Saguenay(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/csd:2494068/council'
  geographic_code = 2494068

  def _get_metadata(self):
    return {
      'name': 'Saguenay',
      'legislature_name': 'Conseil municipal de Saguenay',
      'legislature_url': 'http://ville.saguenay.ca',
    }
