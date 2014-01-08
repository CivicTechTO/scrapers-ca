from utils import CanadianJurisdiction


class GrandePrairieCountyNo1(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/csd:4819006/council'
  geographic_code = 4819006

  def _get_metadata(self):
    return {
      'division_name': 'Grande Prairie County No. 1',
      'name': 'County of Grande Prairie No. 1 Council',
      'url': 'http://www.countygp.ab.ca',
    }
