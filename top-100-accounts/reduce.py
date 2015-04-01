import sys
import time
import struct
import datetime
import hashlib

class Reduce():
  def __init__(self):
    self.retPair = {}

  def getRetPair(self):
    return self.retPair

  def run(self, filename):
    with open('/Users/carl/Desktop/mapPair/' + filename, 'r') as f:
      lines = f.readlines()
    for record in lines:
      rawdata = record.split('|')
      key = (rawdata[0], int(rawdata[1]))
      if rawdata[2][:-1] == 'FALSE':
        value = False
      else:
        value = (int(rawdata[2]),rawdata[3][:-1])
      if not key in self.retPair:
        self.retPair[key] = value
      else:
        del(self.retPair[key])

def main():
  starttime = time.clock()
  
  r = Reduce()

  for i in range(int(sys.argv[1]), int(sys.argv[2]) + 1):
    filename = 'mapPair%.5d.txt' % i
    print filename

    r.run(filename)

    endtime = time.clock()
    print 'RUNTIME:', endtime - starttime
    
  output = r.getRetPair()
  with open('/Users/carl/Desktop/reducePair/reducePair%.5d-%.5d.txt' % (int(sys.argv[1]), int(sys.argv[2])), 'w') as f:
    for record in output:
      if output[record] != False:
        f.write('%s|%d|%d|%s\n' % (record[0], record[1], output[record][0], output[record][1]))
      else:
        f.write('%s|%d|FALSE\n' % (record[0], record[1]))

  print 'REDUCE FINISH'
  endtime = time.clock()
  print 'RUNTIME:', endtime - starttime
  
if __name__ == '__main__':
  main()