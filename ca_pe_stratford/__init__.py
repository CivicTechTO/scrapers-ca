from utils import CanadianJurisdiction


class Stratford(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/csd:1102080/council'
  geographic_code = 1102080

  def _get_metadata(self):
    return {
      'division_name': 'Stratford',
      'name': 'Stratford Town Council',
      'url': 'http://www.townofstratford.ca',
    }
