from utils import CanadianJurisdiction


class LaSalle(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/csd:3537034/council'
  geographic_code = 3537034

  def _get_metadata(self):
    return {
      'name': 'LaSalle',
      'legislature_name': 'LaSalle Town Council',
      'legislature_url': 'http://www.town.lasalle.on.ca',
    }
