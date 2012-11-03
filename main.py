#!/bin/python
from sgu import *
import csv
import shutil
import time
import sys
import os
from rank import *
from datetime import datetime, timedelta
import time

def GetStartTS():
  res = 0
  if FileInCwd('start_timestamp'):
    with open('start_timestamp', 'r') as tsfile:
      res = tsfile.read()
  else:
    res = str(time.time())
    with open('start_timestamp', 'w') as tsfile:
      tsfile.write(res)
  return res

def GetConfig():
  config = {}
  config['start_ts'] = GetStartTS()

  if FileInCwd('contest.conf'):
    with open('contest.conf', 'rb') as csvfile:
      confreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
      config['users'] = confreader.next()
      config['tasks'] = confreader.next()
      config['task_names'] = confreader.next()
      delta = confreader.next()
      start = datetime.fromtimestamp(float(config['start_ts']))
      end = start + timedelta(hours = int(delta[0]), minutes = int(delta[1]), seconds = int(delta[2]))
      config['end_ts'] = str(time.mktime(end.timetuple())) # Unix timestamp
  else:
    print 'Config file missing'
    sys.exit(0)
  return config

def FileInCwd(name):
  return os.path.isfile(os.path.join(os.getcwd(), name))


# write config getting/generation

def WriteRecords(records):
  if FileInCwd('submit.csv'):
    shutil.copy2('submit.csv', ''.join(['submit.', str(time.time()),'.csv']))
  with open('submit.csv', 'wb') as csvfile:
    swriter = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for record in records:
      swriter.writerow(record)


def ReadRecords():
  res = []
  if not FileInCwd('submit.csv'):
    return res
  with open('submit.csv', 'rb') as csvfile:
    sreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in sreader:
      res.append(row)
  return res

def GetSids(records):
  res = []
  for x in records:
    res.append(int(x[0]))
  return res

def RemoveRedundant(records, sids):
  res = []
  for r in records:
    if not (int(r[0]) in sids):
      res.append(r)
  return res

# test that our user did our task and tests finished and error was not funny
def purify(records, config):
  res = []
  # ADD CHECKING FOR TIME
  for row in records:
    if (row[1] in config['users'] and
        str(row[3]) in config['tasks'] and
        str(row[4]) in ['0','2'] and
        float(config['start_ts']) <= float(row[2]) and
        float(row[2]) <= float(config['end_ts'])):
      res.append(row)
  return res


if len(sys.argv) > 1:
  if sys.argv[1] == 'clean':
    for the_file in os.listdir(os.getcwd()):
      file_path = os.path.join(os.getcwd(), the_file)
      if os.path.isfile(file_path) and 'submit' in file_path:
        os.unlink(file_path)
    if FileInCwd('start_timestamp'):
      os.unlink('start_timestamp')
    sys.exit(0)


config = GetConfig()
print 'Contest started at', str(datetime.fromtimestamp(float(config['start_ts'])))
print 'Contest started at', str(datetime.fromtimestamp(float(config['end_ts'])))
print 'Competing users: ', config['users']
print 'Contest exercises: ', config['tasks']

sgu_reader = Sgu()
records_new = sgu_reader.GetRecords()
records_old = ReadRecords()

sids_old = GetSids(records_old)
records_new = RemoveRedundant(records_new, sids_old )

current_records = records_new + records_old


current_records = purify(current_records, config)

current_records = sorted(current_records, key = lambda x : int(x[0]))

WriteRecords(current_records)

rankg = RankGenerator()
ranks = rankg.GenerateRanks(current_records, config)

# render_acm(ranks, config)


