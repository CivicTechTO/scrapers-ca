#!/usr/bin/python
# coding: utf8
from pupa.scrape import Scraper, Legislator
from pupa.models import Organization
from utils import lxmlize

import re

COUNCIL_PAGE = 'http://www.nwtac.com/about/communities/'


class NorthwestTerritoriesPersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)

    councillors = page.xpath('//div[@class="entry-content"]//p/strong')
    for councillor in councillors:
      district = councillor.xpath('./ancestor::p/preceding-sibling::h2')[-1].text_content().split('–'.decode('utf-8'))[0]
      name = ' '.join(councillor.text_content().split()[-2:]).replace('-Â'.decode('utf-8'), '')
      role = councillor.text_content().replace(name, '').split('-')[0]
      if 'SAO' in role or not role:
        continue

      org = Organization(name=district + ' municipal council', classification='legislature', jurisdiction_id=self.jurisdiction.jurisdiction_id)
      org.add_source(COUNCIL_PAGE)
      yield org

      p = Legislator(name=name, post_id=district)
      p.add_source(COUNCIL_PAGE)
      p.add_membership(org, role=role)

      info = councillor.xpath('./ancestor::p/text()')
      for contact in info:
        if 'NT' in contact:
          p.add_contact('address', contact.strip(), 'office')
        if 'Tel' in contact:
          contact = contact.replace('Tel. ', '').replace('(', '').replace(') ', '-').strip()
          p.add_contact('phone', contact, 'office')
        if 'Fax' in contact:
          contact = contact.replace('Fax ', '').replace('(', '').replace(') ', '-').strip()
          p.add_contact('fax', contact, 'office')
      email = councillor.xpath('./parent::p//a[contains(@href, "mailto:")]/text()')[0]
      p.add_contact('email', email, None)

      if 'Website' in councillor.xpath('./parent::p')[0].text_content():
        site = councillor.xpath('./parent::p//a')[1].attrib['href']
        p.add_link(site, 'web page')
      yield p
