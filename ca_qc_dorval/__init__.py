from utils import CanadianJurisdiction


class Dorval(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/csd:2466087/council'
  geographic_code = 2466087

  def _get_metadata(self):
    return {
      'name': 'Dorval',
      'legislature_name': 'Conseil municipal de Dorval',
      'legislature_url': 'http://www.ville.dorval.qc.ca',
    }
