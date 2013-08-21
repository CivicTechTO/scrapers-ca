from utils import CanadianJurisdiction


class Mercier(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/csd:2467045/council'
  geographic_code = 2467045

  def _get_metadata(self):
    return {
      'name': 'Mercier',
      'legislature_name': 'Conseil municipal de Mercier',
      'legislature_url': 'http://www.ville.mercier.qc.ca',
    }
