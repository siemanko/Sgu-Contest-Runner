#!/bin/python
from sgu import *
import csv
import shutil
import time
import sys
import os
from rank import *

tasks = [ '168', '311', '304' ]
users = [ 'Reza_H', 'Andrei Heidelbacher', 'vjudge5' ]

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
def purify(records):
  res = []
  # ADD CHECKING FOR TIME
  for row in records:
    if (row[1] in users) and (str(row[3]) in tasks) and (str(row[4]) in ['0','2']):
      res.append(row)
  return res


if len(sys.argv) > 1:
  if sys.argv[1] == 'clean':
    for the_file in os.listdir(os.getcwd()):
      file_path = os.path.join(os.getcwd(), the_file)
      if os.path.isfile(file_path) and 'submit' in file_path:
        os.unlink(file_path)
    sys.exit(0)

sgu_reader = Sgu()
records_new = sgu_reader.GetRecords()
records_old = ReadRecords()

sids_old = GetSids(records_old)
records_new = RemoveRedundant(records_new, sids_old )

current_records = records_new + records_old


current_records = purify(current_records)

current_records = sorted(current_records, key = lambda x : int(x[0]))

for r in current_records:
  print r

WriteRecords(current_records)



rankg = RankGenerator()
rankg.GenerateRanks(current_records, users, tasks)


