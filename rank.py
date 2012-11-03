# assuming records from lowest sid
class RankGenerator:
  def UpdateTask(self,task, ttime, stype):
    if ('verdict' in task and task['verdict'] == 'Accepted'):
      return
    if stype == '2':
      task['verdict'] = 'FuckUp'
      if not 'bombs' in task:
        task['bombs'] = 1
      else:
        task['bombs'] += 1
    elif stype == '0':
      task['verdict'] = 'Accepted'    
      task['time'] = float(ttime) - float(self.config['start_ts'])
      if not 'bombs' in task:
        task['bombs'] = 0
    else:
      pass

  def AddBombs(self, timestamp, nobombs):
    return timestamp + float(nobombs)*20.0*60.0 # each bomb is 20 minutes

  def GenerateRanks(self, records, config):
    self.config = config
    users = config['users']
    tasks = config['tasks']
    udata = {}
    for u in users:
      udata[u] = {}
      udata[u]['tasks'] = [{} for i in range(len(tasks))]
    taskno = {}
    lastno = 0
    for t in tasks:
      taskno[t]=lastno
      lastno += 1

    for r in records:
      self.UpdateTask(udata[r[1]]['tasks'][taskno[str(r[3])]],r[2], r[4])
      
    res = []
    for u in udata:
      udata[u]['user'] = u
      score = 0
      totaltime = 0.0
      for i in range(len(tasks)):
        if ('verdict' in udata[u]['tasks'][i] and 
            udata[u]['tasks'][i]['verdict'] == 'Accepted'):
          score+=1
          totaltime+=float(udata[u]['tasks'][i]['time'])
          totaltime = self.AddBombs(totaltime, udata[u]['tasks'][i]['bombs'])
      udata[u]['score'] = score
      udata[u]['total_time'] = totaltime
      res.append(udata[u])
    res = sorted(res, key = lambda x: [x['score'], -x['total_time']])

    for x in res:
      print x, '\n\n'
    return res
