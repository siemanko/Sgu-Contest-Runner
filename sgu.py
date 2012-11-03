#!/bin/python
import requests
import csv
from HTMLParser import HTMLParser
from datetime import datetime, timedelta
import time

def parseSaratovDate(datestr):
  return (datetime.strptime(datestr, "%d.%m.%y %H:%M")
          - timedelta(hours = (4-time.timezone)))

# k(kind) : s (start tag), e (end tag), c (content)

class SguAutomata:
  sgu_automata = [
                   { 'k': 's',
                     'v': 'h4'  },
                   { 'k': 'c',
                     'v': 'Status Online' },
                   { 'k': 's',
                     'v': 'table'  },
                   { 'k': 's',
                     'v': 'table'  },
                   { 'k': 's',
                     'v': 'tr'  },
                   { 'k': 'e',
                     'v': 'tr'  }
                 ]
  sgu_automata_index = 0
  sgu_automata_accepting = False
  def is_sgu_automata_accepting(self,k,v):
    if(self.sgu_automata_accepting):
      if k=='e' and v=='table':
        self.sgu_automata_accepting = False
        self.sgu_automata_index = 0
      return self.sgu_automata_accepting
    else:
      if self.sgu_automata_index == len(self.sgu_automata):
        self.sgu_automata_accepting = True
        return True
      if (k == self.sgu_automata[self.sgu_automata_index]['k'] and
          v == self.sgu_automata[self.sgu_automata_index]['v']):
        self.sgu_automata_index += 1
      return False


# 0 - acc, 1 - running, 2 - bomb, 3 - misc
# Bomb: pres, time, wrong, memory
# Ignore: Compilation, *
def decode_result(res):
  if "Accepted" in res:
    return 0
  elif "Running" in res:
    return 1
  elif ("Presentation" in res or
      "Wrong answer" in res or
      "Time Limit Exceeded" in res or
      "Memory Limit Exceeded" in res or
      "Runtime Error" in res):
    return 2
  else:
    return 3

class SubmitionEmiter:
  clolumn_no = 0
  inside_td = False
  s_id = None
  s_author = None
  s_timestamp = None
  s_task = None
  s_result = None
  s_result_array = None
  def get_result(self):
    return self.s_result_array

  def handle_parser_event(self,k, v):
    if(SguAutomata.automata.is_sgu_automata_accepting(k,v)):
      if k=='s':
        if v=='tr':
          self.column_no = 0
        if v=='td':
          self.inside_td = True
      if k=='e':
        if v=='td':
          self.inside_td = False
          self.column_no += 1
        if v=='tr':
          if self.s_result_array == None:
            self.s_result_array = []
          self.s_result_array.append([str(self.s_id),
                                 str(self.s_author),
                                 str(self.s_timestamp),
                                 str(self.s_task),
                                 str(decode_result(self.s_result))])
      if k == 'c' and self.inside_td:
        if self.column_no == 0:
          self.s_id = v.strip()
        if self.column_no == 1:
          # saves unix timestamp in local timezone.
          self.s_timestamp = time.mktime(
                             parseSaratovDate(v.strip()).timetuple())
        if self.column_no == 2:
          self.s_author = v.strip()
        if self.column_no == 3:
          self.s_task = v.strip()
        if self.column_no == 5:
          self.s_result = v

class SguAutomataParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        #print "Encountered a start tag:", tag
        SubmitionEmiter.emiter.handle_parser_event('s', tag)
    def handle_endtag(self, tag):
        #print "Encountered an end tag :", tag
        SubmitionEmiter.emiter.handle_parser_event('e', tag)
    def handle_data(self, data):
        #print "Encountered some data  :", data
        SubmitionEmiter.emiter.handle_parser_event('c', data)

class Sgu:
  def GetRecords(self):
    # instantiate the parser and fed it some HTML
    SguAutomataParser.parser = SguAutomataParser()
    SguAutomata.automata = SguAutomata()
    SubmitionEmiter.emiter = SubmitionEmiter()
    do_once = True
    while(do_once):
      do_once = False
      try:
        r = requests.get('http://acm.sgu.ru/status.php')
      except:
        print 'Error fetching acm.sgu.ru status page'
        continue
      if not r:
        print 'Error fetching acm.sgu.ru status page'
        continue
      SguAutomataParser.parser.feed(r.content)
      return SubmitionEmiter.emiter.get_result()
