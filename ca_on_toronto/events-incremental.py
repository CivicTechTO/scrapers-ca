from __future__ import unicode_literals
from utils import CanadianScraper

from pupa.scrape import Bill, Event
from urllib.parse import parse_qs, urlparse
import lxml.html
import lxml.etree as etree
from collections import defaultdict
import traceback
import datetime as dt
import pytz
import re

from .helpers import (
    committees_from_sessions,
    build_lookup_dict,
    )

from .constants import (
    CALENDAR_DAY_TEMPLATE,
    AGENDA_FULL_STANDARD_TEMPLATE,
    AGENDA_LIST_STANDARD_TEMPLATE,
    AGENDA_FULL_COUNCIL_TEMPLATE,
    AGENDA_LIST_COUNCIL_TEMPLATE,
    AGENDA_ITEM_TEMPLATE,
    COMMITTEE_LIST_TEMPLATE,
    )


STATUS_DICT = {
        'Scheduled': 'confirmed',
        'Scheduled (Preview)': 'confirmed',
        'Complete': 'passed',
        'Cancelled': 'cancelled',
        'No Quorum': 'cancelled',
        'In Recess (will Resume)': 'confirmed',
        'In Progress (Public Session)': 'confirmed',
        }

class TorontoIncrementalEventScraper(CanadianScraper):

    def __init__(self, jurisdiction, datadir, strict_validation=True, fastmode=False):
        super(TorontoIncrementalEventScraper, self).__init__(jurisdiction, datadir, strict_validation=True, fastmode=False)
        # Used to store mappings of committee names to two-letter codes
        self.committees_by_name = {}

    def scrape(self):
        today = dt.datetime.today()
        delta_days = 7
        start_date = today - dt.timedelta(days=delta_days)
        end_date = today + dt.timedelta(days=delta_days*2)

        self.scrape_committee_data()
        yield from self.scrape_events_range(start_date, end_date)

    def scrape_committee_data(self):
        self.committees_by_name = self.committee_lookup_dict()

    def parseCalendarTable(self, table):
        headers = table.xpath(".//th[@class='ss_title_header_top']")
        rows = table.xpath(".//tr[td]")

        keys = []
        for header in headers :
            text_content = header.text_content().replace('&nbsp;', ' ').strip()
            if text_content :
                keys.append(text_content)
            else :
                keys.append(header.xpath('.//input')[0].value)

        for row in rows:
            try:
                data = defaultdict(lambda : None)

                for key, field in zip(keys, row.xpath("./td")):
                    text_content = self._stringify(field)

                    if field.find('.//a') is not None :
                        text_content = self._stringify(field.find('.//a'))
                        address = self._get_link_address(field.find('.//a'))
                        if address :
                            value = {'label': text_content,
                                     'url': address}
                        else :
                            value = text_content
                    else :
                        value = text_content

                    data[key] = value

                yield data, keys, row

            except Exception as e:
                print('Problem parsing row:')
                print(etree.tostring(row))
                print(traceback.format_exc())
                raise e

    def _get_link_address(self, link):
        url = None
        if 'onclick' in link.attrib:
            onclick = link.attrib['onclick']
            if (onclick is not None 
                and onclick.startswith(("radopen('",
                                        "window.open",
                                        "OpenTelerikWindow"))):
                url = self.BASE_URL + onclick.split("'")[1]
        elif 'href' in link.attrib : 
            url = link.attrib['href']

        return url

    def _stringify(self, field) :
        for br in field.xpath("*//br"):
            br.tail = "\n" + br.tail if br.tail else "\n"
        for em in field.xpath("*//em"):
            if em.text :
                em.text = "--em--" + em.text + "--em--"
        return field.text_content().replace('&nbsp;', ' ').strip()

    def extract_events_by_day(self, date):
        url = CALENDAR_DAY_TEMPLATE.format(date.year, date.month-1, date.day)
        page = self.lxmlize(url)

        tables = page.xpath('//table')
        if not tables:
            return []

        table_node = tables[0]

        def sanitize_org_name(org_name):
            # Special case for city council name
            org_name = self.jurisdiction.name if org_name == 'City Council' else org_name
            return org_name

        def sanitize_event(row):
            row['Meeting']['label'] = sanitize_org_name(row['Meeting']['label'])
            return row

        events = [sanitize_event(event) for event, _, _ in self.parseCalendarTable(table_node)]

        return events

    def scrape_events_range(self, start_date, end_date):

        def daterange(start_date, end_date):
            number_of_days = int((end_date - start_date).days)
            for n in range(number_of_days):
                yield start_date + dt.timedelta(n)

        for date in daterange(start_date, end_date):
            events = self.extract_events_by_day(date)
            for event in events:
                meeting_id = parse_qs(urlparse(event['Meeting']['url']).query)['meetingId'][0]
                tz = pytz.timezone("America/Toronto")
                time = dt.datetime.strptime(event['Time'], '%I:%M %p')
                start = tz.localize(date.replace(hour=time.hour, minute=time.minute, second=0, microsecond=0))
                source_url = CALENDAR_DAY_TEMPLATE.format(start.year, start.month, start.day)
                org_name = event['Meeting']['label']
                e = Event(
                    name = org_name,
                    start_time = start,
                    timezone = tz.zone,
                    location_name = event['Location'],
                    status=STATUS_DICT.get(event['Meeting Status'])
                    )
                e.add_source(source_url)
                e.extras = {
                    'meeting_number': event['No.'],
                    'tmmis_meeting_id': meeting_id,
                    }
                e.add_participant(
                    name = org_name,
                    type = 'organization',
                    )

                def is_agenda_available(event):
                    return event['Publishing Status'] in ['Agenda Published', 'Minutes Published']

                def is_council(event):
                    return True if event['Meeting']['label'] == self.jurisdiction.name else False

                if is_agenda_available(event):
                    template = AGENDA_FULL_COUNCIL_TEMPLATE if is_council(event) else AGENDA_FULL_STANDARD_TEMPLATE
                    agenda_url = template.format(meeting_id)
                    full_identifiers = list(self.full_identifiers(meeting_id, is_council(event)))

                    e.add_source(agenda_url)
                    agenda_items = self.agenda_from_url(agenda_url)
                    for i, item in enumerate(agenda_items):

                        a = e.add_agenda_item(item['title'])
                        a.add_classification(item['type'].lower())
                        a['order'] = str(i)

                        def is_vote_event(item):
                            return True if item['type'] == 'ACTION' else False

                        def normalize_wards(raw):
                            if not raw: raw = 'All'
                            if raw == 'All':
                                return raw.lower()
                            else:
                                return raw.split(', ')

                        def is_being_introduced(item, event):
                            org_name = event['Meeting']['label']
                            identifier = item['identifier']

                            # `org_code` is two-letter code for committee
                            current_org_code = self.committees_by_name.get(org_name)[0]['code']
                            originating_org_code = re.search(r'([A-Z]{2})[0-9]+\.[0-9]+', identifier).group(1)

                            return current_org_code == originating_org_code

                        if is_vote_event(item):
                            wards = normalize_wards(item['wards'])
                            identifier_regex = re.compile(r'^[0-9]{4}\.([A-Z]{2}[0-9]+\.[0-9]+)$')
                            [full_identifier] = [id for id in full_identifiers if identifier_regex.match(id).group(1) == item['identifier']]
                            a.add_bill(full_identifier)
                            if is_being_introduced(item, event):
                                b = Bill(
                                    # TODO: Fix this hardcode
                                    legislative_session = '2014-2018',
                                    identifier = full_identifier,
                                    title = item['title'],
                                    from_organization = {'name': org_name},
                                    )
                                b.add_source(agenda_url)
                                b.add_document_link(note='canonical', media_type='text/html', url=AGENDA_ITEM_TEMPLATE.format(full_identifier))
                                b.extras = {
                                    'wards': wards,
                                    }

                                yield b

                yield e

    def agenda_from_url(self, url):
        page = self.lxmlize(url)
        main = page.xpath('//table[1]/..')[0]
        top_level_elems = main.getchildren()
        section_breaks = page.cssselect('table.border')

        section_break_indices = [i for i, elem in enumerate(top_level_elems) if elem in section_breaks]

        def partition(alist, indices): return [alist[i:j] for i, j in zip([0]+indices, indices+[None])]

        sections = partition(top_level_elems, section_break_indices)

        def treeify_section_list(section):
            tree = lxml.html.Element('section')
            for elem in section:
                tree.append(elem)

            return tree

        section_trees = [treeify_section_list(section) for section in sections]

        preamble = section_trees.pop(0)
        agenda_items = section_trees

        items = []
        newline_regex = re.compile(r' ?\r\n ?')
        for item in agenda_items:
            dict = {
                    'identifier': item.xpath('//table[1]//td[1]')[0].text_content(),
                    'type': item.xpath('//table[1]//td[2]')[0].text_content().strip(),
                    'wards': item.xpath('//table[1]//td[5]')[0].text_content().strip().replace('Ward:',''),
                    'title': newline_regex.sub(' ', item.xpath('//table[2]//td[1]')[0].text_content().strip()),
                    }

            items.append(dict)

        return items

    def committee_lookup_dict(self):
        # reversed so that most recent first
        sessions = reversed(self.jurisdiction.legislative_sessions)
        committee_term_instances = committees_from_sessions(self, sessions)
        committees_by_name = build_lookup_dict(self, data_list=committee_term_instances, index_key='name')
        # Manually add our City Council exception.
        committees_by_name.update({ self.jurisdiction.name: [{'code':'CC'}] })

        return committees_by_name

    def full_identifiers(self, meeting_id, is_council=False, url=None):
        if not url:
            template = AGENDA_LIST_COUNCIL_TEMPLATE if is_council else AGENDA_LIST_STANDARD_TEMPLATE
            url = template.format(meeting_id)

        page = self.lxmlize(url)
        for a in page.xpath('//table[@class="itemTable"]//td[@class="itemNum"]//a'):
            link = a.attrib['href']
            full_identifier = parse_qs(urlparse(link).query)['item'][0]
            yield full_identifier
