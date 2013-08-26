from pupa.scrape import Scraper, Legislator

from utils import lxmlize, CanadianScraper

import re

COUNCIL_PAGE = 'http://www.ville.mercier.qc.ca/02_viedemocratique/default.asp'


class MercierPersonScraper(CanadianScraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)
    organization = self.get_organization()
    yield organization

    councillors = page.xpath('//table//tr[2]//table//td')
    for councillor in councillors:
      if not councillor.text_content().strip():
        continue

      if councillor == councillors[6]:
        name = councillor.xpath('.//span')[0].text_content().replace('Maire', '').strip()
        district = 'mercier'
        role = 'mayor'
      else:
        name, district = councillor.xpath('.//span')[0].text_content().split('Conseiller')
        name = name.replace('Monsieur', '').replace('Madame', '').strip()
        district = district.strip()
        role = 'councillor'
      email = councillor.xpath('.//a[contains(@href, "mailto:")]/@href')[0].replace('mailto:', '')

      p = Legislator(name=name, post_id=district)
      p.add_source(COUNCIL_PAGE)
      p.add_membership(organization, role=role)
      p.add_contact('email', email, None)
      p.image = councillor.xpath('.//img/@src')[0]
      yield p
