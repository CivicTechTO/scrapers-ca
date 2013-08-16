from utils import CanadianJurisdiction

class GrandePrairieCountyNo1(CanadianJurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/csd:4819006/council'
  geographic_code = 4819006
  def _get_metadata(self):
    return {
      'name': 'Grande Prairie County No. 1',
      'legislature_name': 'Grande Prairie County No. 1 City Council',
      'legislature_url': 'http://cms.burlington.ca/Page110.aspx',
    }
