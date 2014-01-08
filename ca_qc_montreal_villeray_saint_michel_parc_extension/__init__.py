# coding: utf8
from ca_qc_montreal import MontrealPersonScraper
from utils import CanadianJurisdiction


class VilleraySaintMichelParcExtension(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/csd:2466023/arrondissement:villeray-saint-michel-parc-extension/council'
  ocd_division = 'ocd-division/country:ca/csd:2466023/arrondissement:villeray-saint-michel-parc-extension'

  def _get_metadata(self):
    return {
      'division_name': u'Villeray—Saint-Michel—Parc-Extension',
      'name': u"Conseil d'arrondissement de Villeray—Saint-Michel—Parc-Extension",
      'url': 'http://ville.montreal.qc.ca/vsp',
      'provides': ['people'],
    }

  def get_scraper(self, term, session, scraper_type):
    if scraper_type == 'people':
        return MontrealPersonScraper
