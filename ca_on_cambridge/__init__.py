from utils import CanadianJurisdiction


class Cambridge(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/csd:3530010/council'
  geographic_code = 3530010

  def _get_metadata(self):
    return {
      'name': 'Cambridge',
      'legislature_name': 'Cambridge City Council',
      'legislature_url': 'http://www.cambridge.ca',
    }
