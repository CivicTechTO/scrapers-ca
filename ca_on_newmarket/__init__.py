from utils import CanadianJurisdiction


class Newmarket(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/csd:3519048/council'
  geographic_code = 3519048

  def _get_metadata(self):
    return {
      'name': 'Newmarket',
      'legislature_name': 'Newmarket Town Council',
      'legislature_url': 'http://www.town.newmarket.on.ca',
    }
