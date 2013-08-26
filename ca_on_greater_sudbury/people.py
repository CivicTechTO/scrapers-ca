from pupa.scrape import Scraper, Legislator

from utils import lxmlize, CanadianScraper

import re

COUNCIL_PAGE = 'http://www.greatersudbury.ca/inside-city-hall/city-council/'


class GreaterSudburyPersonScraper(CanadianScraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)
    organization = self.get_organization()
    yield organization

    councillors = page.xpath('//div[@id="navMultilevel"]//a')
    for councillor in councillors:
      if councillor == councillors[0]:
        yield self.scrape_mayor(councillor, organization)
        continue

      if not '-' in councillor.text_content():
        break

      district, name = councillor.text_content().split(' - ')

      page = lxmlize(councillor.attrib['href'])

      address = page.xpath('//div[@class="column last"]//p')[0].text_content()
      phone = page.xpath('//article[@id="primary"]//*[contains(text(),"Tel")]')[0].text_content()
      phone = re.findall(r'([0-9].*)', phone)[0].replace(') ', '-')
      fax = page.xpath('//article[@id="primary"]//*[contains(text(),"Fax")]')[0].text_content()
      fax = re.findall(r'([0-9].*)', fax)[0].replace(') ', '-')
      email = page.xpath('//a[contains(@href, "mailto:")]')[0].text_content()

      p = Legislator(name=name, post_id=district)
      p.add_source(COUNCIL_PAGE)
      p.add_source(councillor.attrib['href'])
      p.add_membership(organization, role='councillor')
      p.add_contact('address', address, 'City Council general mailing address')
      p.add_contact('phone', phone, 'office')
      p.add_contact('fax', fax, 'office')
      p.add_contact('email', email, 'office')
      p.image = page.xpath('//article[@id="primary"]//img/@src')[1]
      yield p

  def scrape_mayor(self, div, organization):
    url = div.attrib['href']
    page = lxmlize(url)

    name = div.text_content().replace('Mayor ', '')
    contact_url = page.xpath('//ul[@class="navSecondary"]//a[contains(text(),"Contact")]')[0].attrib['href']
    page = lxmlize(contact_url)

    contact_div = page.xpath('//div[@class="col"][2]')[0]

    address = contact_div.xpath('.//p[1]')[0].text_content()
    address = re.findall(r'(City of Greater .*)', address, flags=re.DOTALL)[0]
    phone = contact_div.xpath('.//p[2]')[0].text_content()
    phone = phone.replace('Phone: ', '')
    fax = contact_div.xpath('.//p[3]')[0].text_content()
    fax = fax.split(' ')[-1]
    email = contact_div.xpath('//a[contains(@href, "mailto:")]')[0].text_content()

    p = Legislator(name=name, post_id='Sudbury')
    p.add_source(COUNCIL_PAGE)
    p.add_source(contact_url)
    p.add_membership(organization, role='mayor')
    p.add_contact('address', address, 'office')
    p.add_contact('phone', phone, 'office')
    p.add_contact('fax', fax, 'office')
    p.add_contact('email', email, None)
    return p
