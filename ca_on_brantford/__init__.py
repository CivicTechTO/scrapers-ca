from utils import CanadianJurisdiction


class Brantford(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/csd:3529006/council'
  geographic_code = 3529006

  def _get_metadata(self):
    return {
      'division_name': 'Brantford',
      'name': 'Brantford City Council',
      'url': 'http://www.city.brantford.on.ca',
    }
