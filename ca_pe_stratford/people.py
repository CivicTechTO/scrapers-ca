from pupa.scrape import Scraper, Legislator

from utils import lxmlize, CanadianScraper

import re

COUNCIL_PAGE = 'http://www.townofstratford.ca/town-hall/government/town-council/'


class StratfordPersonScraper(CanadianScraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)
    organization = self.get_organization()
    yield organization

    yield self.scrape_mayor(page, organization)

    councillors = page.xpath('//strong[contains(text(), "Councillor")]/parent::p')
    for councillor in councillors:

      name = councillor.xpath('./strong/text()')[0].replace('Councillor', '')
      district = re.findall('Ward .*', councillor.text_content())[0]

      p = Legislator(name=name, post_id=district)
      p.add_source(COUNCIL_PAGE)
      p.add_membership(organization, role='councillor')

      p.image = councillor.xpath('./img/@src')[0]

      phone = re.findall(r'Phone(.*)', councillor.text_content())
      if not phone:
        phone = re.findall(r'Phone(.*)', councillor.xpath('./following-sibling::p')[1].text_content())
      phone = phone[0].strip()

      email = councillor.xpath('.//a[contains(@href, "mailto:")]')
      if not email:
        email = councillor.xpath('./following-sibling::p//a[contains(@href, "mailto")]')
      email = email[0].text_content()

      p.add_contact('phone', phone, 'office')
      p.add_contact('email', email, None)

      yield p

  def scrape_mayor(self, page, organization):
    info = page.xpath('//div[@class="entry-content"]/p')[:4]
    name = info[0].text_content().replace('Mayor', '')
    email = info[2].xpath('./a')[0].text_content()
    phone = info[3].text_content().replace('Phone ', '')

    p = Legislator(name=name, post_id='stratford')
    p.add_source(COUNCIL_PAGE)
    p.add_membership(organization, role='mayor')
    p.image = page.xpath('//div[@class="entry-content"]/p/a/img/@src')[0]
    p.add_contact('email', email, None)
    p.add_contact('phone', phone, 'office')
    return p
