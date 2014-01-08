from utils import CanadianJurisdiction


class Edmonton(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/csd:4811061/council'
  geographic_code = 4811061

  def _get_metadata(self):
    return {
      'division_name': 'Edmonton',
      'name': 'Edmonton City Council',
      'url': 'http://www.edmonton.ca',
    }
