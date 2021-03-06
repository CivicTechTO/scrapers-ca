from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

import re

COUNCIL_PAGE = 'http://www.laval.ca/Pages/Fr/A-propos/conseillers-municipaux.aspx'


class LavalPersonScraper(CanadianScraper):

    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        for councillor_row in page.xpath('//tr'):
            post = list(filter(None, (text.strip() for text in councillor_row.xpath('./td[2]/p/text()'))))[0]
            if post == 'Maire de Laval':
                district = 'Laval'
                role = 'Maire'
            else:
                district = re.sub(r'District.\d+.- ', '', post).replace("L'", '').replace(' ', '').replace('bois', 'Bois')
                role = 'Conseiller'
            full_name = list(filter(None, (text.strip() for text in councillor_row.xpath('./td[2]/p/text()'))))[1].strip()
            name = ' '.join(full_name.split()[1:])

            phone = councillor_row.xpath('.//span[@class="icon-phone"]/following::text()')[0]
            email = self.get_email(councillor_row)
            photo_url = councillor_row[0][0].attrib['src']
            p = Person(primary_org='legislature', name=name, district=district, role=role, image=photo_url)
            p.add_source(COUNCIL_PAGE)
            p.add_contact('voice', phone, 'legislature')
            p.add_contact('email', email)
            yield p
