from utils import CanadianJurisdiction


class Wilmot(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/csd:3530020/council'
  geographic_code = 3530020

  def _get_metadata(self):
    return {
      'division_name': 'Wilmot',
      'name': 'Wilmot Township Council',
      'url': 'http://www.wilmot.ca',
    }
