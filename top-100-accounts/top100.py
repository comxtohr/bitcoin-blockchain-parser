import sys
import time
import operator

class Top100:
  def __init__(self):
    self.balance = {}

  def getBalance(self):
    return self.balance

  def run(self, filename):
    with open('/Users/carl/Desktop/reduce^3Pair/' + filename, 'r') as f:
      lines = f.readlines()
    for record in lines:
      rawdata = record.split('|')
      key = (rawdata[0], int(rawdata[1]))
      if rawdata[2][:-1] == 'FALSE':
        continue
      value = (int(rawdata[2]),rawdata[3][:-1])
      if not value[1] in self.balance:
      	self.balance[value[1]] = 0
      self.balance[value[1]] += value[0]

def main():
  starttime = time.clock()
  filename = 'reducePair%.5d-%.5d.txt' % (int(sys.argv[1]), int(sys.argv[2]))
  print filename

  top100 = Top100()
  top100.run(filename)

  balance = top100.getBalance()

  t = 0
  output = sorted(balance.iteritems(), key = operator.itemgetter(1), reverse=True)
  
  print 'GET TOP 100'
  endtime = time.clock()
  print 'RUNTIME:', endtime - starttime

  with open('/Users/carl/Desktop/top100.txt', 'w') as f:
    for record in output:
      f.write('%d %s\n' % (record[1], record[0].encode('hex_codec')))
      t += 1
      if t == 500: break

  endtime = time.clock()
  print 'RUNTIME:', endtime - starttime

if __name__ == '__main__':
  main()