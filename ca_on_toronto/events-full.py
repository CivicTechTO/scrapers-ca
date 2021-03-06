from __future__ import unicode_literals

from pupa.scrape import Event
from utils import CanadianScraper

import re
import datetime as dt
import csv
import tempfile
import shutil
import os
import pytz


class TorontoFullEventScraper(CanadianScraper):
    # Start of 2014-2018 legislative session
    start_date = dt.datetime(2014, 12, 1)
    end_date = dt.datetime(2018, 11, 30)
    quick_agenda = True

    def scrape(self):
        "http://app.toronto.ca/tmmis/getAdminReport.do?function=prepareMeetingScheduleReport"
        "http://app.toronto.ca/tmmis/getAdminReport.do?function=prepareMemberAttendanceReport"

        # scrape attendance

        tmpdir = tempfile.mkdtemp()

        page = self.lxmlize("http://app.toronto.ca/tmmis/getAdminReport.do?function=prepareMemberAttendanceReport")
        members = page.xpath('//td[@class="inputText"]/select[@name="memberId"]/option')
        for member in members:
            if member.attrib['value'] == 0:
                continue
            post = {
                'function': 'getMemberAttendanceReport',
                'download': 'csv',
                'termId': 6,
                'memberId': member.attrib['value'],
                'decisionBodyId': 0,
                'fromDate': self.start_date.strftime('%F'),
                'toDate': self.end_date.strftime('%F'),
            }
            r = self.post("http://app.toronto.ca/tmmis/getAdminReport.do", data=post)
            if r.headers['content-type'] != 'application/vnd.ms-excel':
                continue

            attendance_file = open(tmpdir + '/' + member.text + '.csv', 'w')
            attendance_file.write(r.text)
            attendance_file.close()

        # scrape events
        post = {
            'function': 'getMeetingScheduleReport',
            'download': 'csv',
            'termId': 6,
            'decisionBodyId': 0,
            'fromDate': self.start_date.strftime('%F'),
            'toDate': self.end_date.strftime('%F'),
        }

        r = self.post("http://app.toronto.ca/tmmis/getAdminReport.do", data=post)
        empty = []

        meeting_file = open('meetings.csv', 'w')
        meeting_file.write(r.text)
        meeting_file.close()
        with open('meetings.csv', 'rt') as csvfile:
            csvfile = csv.reader(csvfile, delimiter=',')
            next(csvfile)

            committee = ''
            agenda_items = []

            for row in csvfile:
                name = row[0]
                when = row[2]
                when = dt.datetime.strptime(when, "%Y-%m-%d")
                time = row[3]
                time = dt.datetime.strptime(time, "%I:%M %p")
                location = row[5]

                if name != committee:
                    committee = name
                    agenda_items = self.find_items(committee)

                tz = pytz.timezone("America/Toronto")
                start = tz.localize(when.replace(hour=time.hour, minute=time.minute))

                normalized_name = self.jurisdiction.name if name == 'City Council' else name

                e = Event(
                    name=normalized_name,
                    start_time=start,
                    location_name=location,
                    timezone=tz.zone,
                    status=confirmedOrPassed(start),
                )
                e.add_committee(normalized_name)

                attendees = self.find_attendees(tmpdir, row)
                if len(attendees) == 0:
                    empty.append(row)
                for attendee in self.find_attendees(tmpdir, row):
                    e.add_person(attendee)
                e.add_source("http://app.toronto.ca/tmmis/getAdminReport.do?function=prepareMeetingScheduleReport")

                for item in agenda_items:
                    if item['date'].date() == when.date():
                        i = e.add_agenda_item(item['description'])
                        i.add_committee(normalized_name)
                        i['order'] = item['order']
                        i.add_bill(i['order'])

                        for link in item['links']:
                            # Max 300 char for DB field
                            if len(link['name']) > 300:
                                link['name'] = link['name'][:299] + '…'
                            i.add_media_link(link['name'], link['url'], on_duplicate='ignore', media_type='')

                        if 'notes' in item:
                            i['notes'] = [item['notes']]

                yield e

        shutil.rmtree(tmpdir)
        os.remove('meetings.csv')

    def find_attendees(self, directory, event):
        # TODO
        # go through all csv files and find members that attended the event
        attendees = []
        files = [f for f in os.listdir(directory)]
        for f in files:
            name = f.replace('.csv', '')
            with open(directory + '/' + f, 'rt') as csvfile:
                csvfile = csv.reader(csvfile, delimiter=',')
                next(csvfile)
                for row in csvfile:
                    # find the right date
                    if row[2] == event[2]:
                        if (row[0] == event[0]) and (row[1] == event[1]) and (row[5] == "Y"):
                            attendees.append(name)
        return set(attendees)

    def find_items(self, committee):

        agenda_items = []

        page = self.lxmlize('http://app.toronto.ca/tmmis/decisionBodyList.do?function=prepareDisplayDBList')
        link = page.xpath('//table[@class="default zebra"]//a[contains(text(),"{}")]/@href'.format(committee))
        if link:
            link = link[0]
        else:
            return None

        page = self.lxmlize(link)
        meetings = page.xpath('//a[contains(@name, "header")]')
        for meeting in meetings:
            meeting_header = meeting.xpath('./parent::h3')[0].text_content()
            if all(status not in meeting_header for status in ['Complete', 'Scheduled (Preview)']):
                continue
            date = meeting.xpath('./parent::h3')[0].text_content().strip().split('-')
            date = dt.datetime.strptime('-'.join(date[0:2]).strip(), "%B %d, %Y - %I:%M %p")
            if date < self.start_date or date > self.end_date:
                continue
            meeting_id = meeting.attrib['name'].replace('header', '').strip()
            # get = { 'function' : 'doPrepare', 'meetingId' : meeting_id }
            if committee == 'City Council':
                request_string = 'http://app.toronto.ca/tmmis/viewAgendaItemList.do?function=getCouncilAgendaItems&meetingId={}'.format(meeting_id)
            else:
                request_string = 'http://app.toronto.ca/tmmis/viewAgendaItemList.do?function=getAgendaItems&meetingId={}'.format(meeting_id)
            page = self.lxmlize(request_string)

            items = page.xpath('//tr[contains(@class, "item_")]')
            for item in items:
                root_link = item.xpath('.//a/@href')[0]
                root_description = item.xpath('./td[contains(@class, "itemDesc")]/span[1]/text()')[0]
                #root_description = ' '.join(root_description.split('&nbsp;')[:-1]).strip()
                agenda_item_identifier = root_link.split('?')[-1].split('=')[-1]
                root_order = agenda_item_identifier

                if self.quick_agenda:
                    agenda_item = {
                        'committee': committee,
                        'description': root_description,
                        'order': root_order,
                        'date': date,
                        'links': [],
                    }
                    agenda_items.append(agenda_item)
                    continue

                page = self.lxmlize(root_link)
                item_content_script = page.xpath('//script[contains(text(), "loadContent")]/text()')[0]
                item_id = re.findall(r'(?<=agendaItemId:")(.*)(?=")', item_content_script)[0]
                if committee == 'City Council':
                    item_info_url = 'http://app.toronto.ca/tmmis/viewAgendaItemDetails.do?function=getCouncilMinutesItemPreview&agendaItemId={}'.format(item_id)
                else:
                    item_info_url = 'http://app.toronto.ca/tmmis/viewAgendaItemDetails.do?function=getMinutesItemPreview&agendaItemId={}'.format(item_id)
                page = self.lxmlize(item_info_url)

                root_description = page.xpath('//font[@size="4"]')[0].text_content()

                # Get background documents
                item_links = []
                links = page.xpath('//a[not(contains(@href, "mailto:"))]')
                for link in links:
                    if 'href' not in list(link.attrib.keys()):
                        continue
                    description = link.xpath('.//parent::font/preceding-sibling::font/text()')
                    if description:
                        description = description[-1]
                    else:
                        description = link.text_content()
                    item_link = {'name': description, 'url': link.attrib['href']}
                    item_links.append(item_link)

                agenda_item = {
                    'committee': committee,
                    'description': root_description,
                    'order': root_order,
                    'date': date,
                    'links': item_links,
                }

                agenda_items.append(agenda_item)

                # Read through the decisions section and create agenda items from the list
                decisions = page.xpath('//b[contains(text(), "Decision")]/ancestor::tr/following-sibling::tr//p')
                agenda_item = {}
                notes = ''
                for decision in decisions:
                    if 'style' in list(decision.attrib.keys()) and 'MARGIN-LEFT: 1in' in decision.attrib['style']:
                        note = decision.text_content().strip()
                        notes = notes + ' ' + note
                    if not decision.text_content().strip() or not re.findall(r'[0-9]\.\W{2,}', decision.text_content()):
                        continue
                    number = re.findall(r'([0-9]{1,2})\.', decision.text_content())[0]
                    description = re.sub(r'^[0-9]{1,2}\.', '', decision.text_content()).strip()
                    order = root_order + '-' + number

                    agenda_item['committee'] = committee
                    agenda_item['description'] = description
                    if len(notes) > 0:
                        agenda_item['notes'] = {'description': notes}
                    agenda_item['order'] = order
                    agenda_item['date'] = date
                    agenda_item['links'] = item_links
                    agenda_items.append(agenda_item)
                    agenda_item = {}
                    notes = ''

        return agenda_items


def confirmedOrPassed(when):
    if dt.datetime.utcnow().replace(tzinfo=pytz.utc) < when:
        status = 'confirmed'
    else:
        status = 'passed'

    return status
