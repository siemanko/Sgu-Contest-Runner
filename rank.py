

UpdateTask

# assuming records from lowest sid
class RankGenerator:
  def GenerateRanks(self, records,users,tasks):
    udata = {}
    for u in users:
      udata[u] = {}
      udata[u]['tasks'] = [{}] * len(tasks)
    taskno = {}
    lastno = 0
    for t in tasks:
      taskno[t]=lastno
      lastno += 1

    for r in records:
      UpdateTask(udata[r[1]]['tasks'][taskno[int(r[3])]],r[3], r[4])
      
