from pupa.scrape import Scraper, Legislator
from pupa.models import Organization

from utils import lxmlize
from utils import CanadianScraper
import re

COUNCIL_PAGE = 'http://www.edmonton.ca/city_government/city_organization/city-councillors.aspx'
MAYOR_PAGE = 'http://www.edmonton.ca/city_government/city_organization/the-mayor.aspx'


class EdmontonPersonScraper(CanadianScraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)
    organization = self.get_organization()
    yield organization

    yield scrape_mayor(organization)
    councillors = page.xpath('//div[@id="contentArea"]//h3//a/@href')
    for councillor in councillors:
      page = lxmlize(councillor)
      district, name = page.xpath('//div[@id="contentArea"]/h1/text()')[0].split('-')

      p = Legislator(name=name, post_id=district)
      p.add_source(COUNCIL_PAGE)
      p.add_source(councillor)
      p.add_membership(organization, role='councillor')

      image = page.xpath('//div[@id="contentArea"]//img/@src')
      if image:
        p.image = image[0]

      address = page.xpath('//address//p')
      if address:
        address = address[0].text_content()
        p.add_contact('address', address, 'office')

      contacts = page.xpath('//table[@class="contactListing"]//tr')
      for contact in contacts:
        contact_type = contact.xpath('./th/text()')[0]
        value = contact.xpath('./td//text()')[0]
        if 'Title' in contact_type:
          continue
        if 'Website' in contact_type or 'Facebook' in contact_type or 'Twitter' in contact_type:
          value = contact.xpath('./td/a/text()')[0]
          p.add_link(value, contact_type)
          continue
        p.add_contact(contact_type, value, 'office')
      print p._contact_details
      yield p


def scrape_mayor(organization):
  page = lxmlize(MAYOR_PAGE)
  name = page.xpath('//strong[contains(text(), "Mayor")]/text()')[1].replace('Mayor', '').strip()

  p = Legislator(name=name, post_id='edmonton')
  p.add_source(MAYOR_PAGE)
  p.add_membership(organization, role='mayor')

  image = page.xpath('//div[@id="contentArea"]//img/@src')[0]
  p.image = image

  address = ' '.join(page.xpath('//address/p/text()'))
  phone = page.xpath('.//address/following-sibling::table/tbody/tr/td/text()')[0]
  fax = page.xpath('.//address/following-sibling::table/tbody/tr/td/text()')[1]

  p.add_contact('address', address, 'office')
  p.add_contact('phone', phone, 'office')
  p.add_contact('fax', fax, 'office')

  return p
