from utils import CanadianJurisdiction


class Milton(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/csd:3524009/council'
  geographic_code = 3524009

  def _get_metadata(self):
    return {
      'division_name': 'Milton',
      'name': 'Milton Town Council',
      'url': 'http://www.milton.ca',
    }
