from pupa.scrape import Scraper, Legislator

from utils import lxmlize, CanadianScraper

import re

COUNCIL_PAGE = 'http://www.pickering.ca/en/cityhall/citycouncil.asp'


class PickeringPersonScraper(CanadianScraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)
    organization = self.get_organization()
    yield organization

    mayor_contacts = page.xpath('//table[@class="nicEdit-visualClass"]//tr/td[1]/text()')
    council_contacts = page.xpath('//table[@class="nicEdit-visualClass"]//tr/td[2]/text()')

    councillors = page.xpath('//table[@id="Table3table"]//strong/ancestor::td')
    for councillor in councillors:
      name = councillor.xpath('.//strong/text()')[0]
      if 'Councillor' in name:
        name = name.replace('Councillor', '').strip()
        role_ward = councillor.xpath('./text()')[0]
        if not role_ward.strip():
          role_ward = councillor.xpath('.//p/text()')[0]
        role_ward = role_ward.split(' ')
        role = ' '.join(role_ward[:2])
        ward = ' '.join(role_ward[2:])
      else:
        name = councillor.xpath('.//strong/text()')[1]
        role = 'mayor'
        ward = 'pickering'
      email = councillor.xpath('.//a[contains(@href, "mailto:")]/text()')[0]
      p = Legislator(name=name, post_id=ward)
      p.add_source(COUNCIL_PAGE)
      p.add_membership(organization, role=role)
      p.add_contact('email', email, None)
      p.image = councillor.xpath('.//img/@src')[0]

      links = councillor.xpath('.//a')
      for link in links:
        if '@' in link.text_content():
          continue
        if 'Profile' in link.text_content():
          p.add_source(link.attrib['href'])
        else:
          p.add_link(link.attrib['href'], 'personal site')

      if role == 'mayor': 
        add_contacts(p, mayor_contacts)
      else: 
        add_contacts(p, council_contacts)
      yield p


def add_contacts(p, contacts):
  phone = re.findall(r'[0-9]{3}\.[0-9]{3}\.[0-9]{4}', contacts[0])[0]
  fax = re.findall(r'[0-9]{3}\.[0-9]{3}\.[0-9]{4}', contacts[1])[0]
  p.add_contact('phone', phone, 'office')
  p.add_contact('fax', fax, 'office')


      