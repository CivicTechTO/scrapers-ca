from utils import CanadianJurisdiction


# The official government sources lists only top-level officials.
# @see http://www.maca.gov.nt.ca/
class NorthwestTerritories(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/territory:nt/legislature'

  def _get_metadata(self):
    return {
      'division_name': 'Northwest Territories',
      'name': 'Northwest Territories City Council',
      'url': 'http://www.nwtac.com/about/communities/',
    }
