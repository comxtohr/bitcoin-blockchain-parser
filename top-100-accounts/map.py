import sys
import time
import struct
import datetime
import hashlib

class Map():
  
  def __init__(self, tid, filename):
    self.tid = tid
    self.filename = filename
    self.retPair = {}

  def getRetPair(self):
    return self.retPair

  def uint8_t(self, stream):
    return ord(stream.read(1))

  def uint16_t(self, stream):
    return struct.unpack('H', stream.read(2))[0]

  def uint32_t(self, stream):
    return struct.unpack('I', stream.read(4))[0]

  def uint64_t(self, stream):
    return struct.unpack('Q', stream.read(8))[0]

  def hash32(self, stream):
    return stream.read(32)[::-1]

  def varint(self, stream):
    size = self.uint8_t(stream)
    if size < 0xfd: return size
    if size == 0xfd: return self.uint16_t(stream)
    if size == 0xfe: return self.uint32_t(stream)
    if size == 0xff: return self.uint64_t(stream)

  def packWithVarint(self, k):
    if k < 0xfd: return struct.pack('B', k)
    if k <= 0xffff: return '\xfd' + struct.pack('H', k)
    if k <= 0xffffffff: return '\xfe' + struct.pack('I', k)
    return '\xff' + struct.pack('Q', k)

  def magicid(self, stream):
    buf = stream.read(4)
    if buf == '':
      return -1
    else:
      return struct.unpack('I', buf)[0]

  def script(self, stream, length):
    return stream.read(length)

  def timestr(self, buf):
    return datetime.datetime.fromtimestamp(buf)

  def run(self):
    total = 0
    with open('/Users/carl/Library/Application Support/Bitcoin/blocks/' + self.filename, 'rb') as f:
      while True:
        magicID = self.magicid(f)
        if magicID == -1:
          break
        else:
          total += 1
        headerLength = self.uint32_t(f)
        versionNumber = self.uint32_t(f)
        prevHash = self.hash32(f)
        merkleRoot = self.hash32(f)
        timeStamp = self.uint32_t(f)
        difficulty = self.uint32_t(f)
        nonce = self.uint32_t(f)
        #blockBin = struct.pack('I32s32sIII',versionNumber, prevHash[::-1], merkleRoot[::-1], timeStamp, difficulty, nonce)
        #blockHash = hashlib.sha256(hashlib.sha256(blockBin).digest()).digest()[::-1]
        transactionCount = self.varint(f)
        #print 'magicID:', magicID
        #print 'headerLength:', headerLength
        #print 'versionNumber:', versionNumber
        #print 'prevHash:', prevHash.encode('hex_codec')
        #print 'merkleRoot:', merkleRoot.encode('hex_codec')
        #print 'timeStamp:', timestr(timeStamp)
        #print 'difficulty:', difficulty
        #print 'nonce:', nonce
        #print 'transactionCount:', transactionCount
        #print 'blockHash:', blockHash.encode('hex_codec')
        #print '============Transaction============'
        for i in range(transactionCount):
          transactionVersionNumber = self.uint32_t(f)
          inputCount = self.varint(f)
          transactionBin = struct.pack('I', transactionVersionNumber) + self.packWithVarint(inputCount)
          #print 'transactionVersionNumber:', transactionVersionNumber
          #print 'inputCount:', inputCount
          #print '---------------Input---------------'
          for j in range(inputCount):
            inputTransactionHash = self.hash32(f)
            transactionIndex = self.uint32_t(f)
            scriptLength = self.varint(f)
            inputScript = self.script(f, scriptLength)
            sequenceNumber = self.uint32_t(f)
            transactionBin = transactionBin + inputTransactionHash[::-1] + struct.pack('I', transactionIndex) + self.packWithVarint(scriptLength) + inputScript + struct.pack('I', sequenceNumber)
            key = (inputTransactionHash, transactionIndex)
            if not key in self.retPair:
              self.retPair[key] = False
            else:
              del(self.retPair[key])

            #print 'inputTransactionHash:', inputTransactionHash.encode('hex_codec')
            #print 'transactionIndex:', ('%x' % transactionIndex)
            #print 'scriptLength:', scriptLength
            #print 'inputScript:', inputScript.encode('hex_codec')
            #print 'sequenceNumber:', ('%x' % sequenceNumber)
            #print '-----------------------------------'
          outputCount = self.varint(f)
          transactionBin = transactionBin + self.packWithVarint(outputCount)
          flag = 0
          #print 'outputCount:', outputCount
          #print '--------------Output---------------'
          output = []
          for j in range(outputCount):
            value = self.uint64_t(f)
            outputScriptLength = self.varint(f)
            outputScript = self.script(f,outputScriptLength)
            
            output.append((j, value, outputScript))

            transactionBin = transactionBin + struct.pack('Q', value) + self.packWithVarint(outputScriptLength) + outputScript
            #print 'value:', value
            #print 'outputScriptLength:', outputScriptLength
            #print 'value:', value
            #print 'outputScript', outputScript.encode('hex_codec')
            #print '-----------------------------------'
          transactionLockTime = self.uint32_t(f)
          transactionBin = transactionBin + struct.pack('I', transactionLockTime)
          transactionHash = hashlib.sha256(hashlib.sha256(transactionBin).digest()).digest()[::-1]

          for record in output:
            key = (transactionHash, record[0])
            if not key in self.retPair:
              self.retPair[key] = (record[1], record[2])
            else:
              del(self.retPair[key])
          #print 'transactionLockTime:', transactionLockTime
          #print 'transactionHash:', transactionHash.encode('hex_codec')
          #print '==================================='
    #print 'total:', total

def main():
  starttime = time.clock()

  for i in range(int(sys.argv[1]), int(sys.argv[2]) + 1):
    filename = 'blk%.5d.dat' % i
    print filename
    
    m = Map(i, filename)
    m.run()

    output = m.getRetPair()
    with open('/Users/carl/Desktop/mapPair/mapPair%.5d.txt' % i, 'w') as f:
      for record in output:
        if output[record] != False:
          f.write('%s|%d|%d|%s\n' % (record[0].encode('hex_codec'), record[1], output[record][0], output[record][1].encode('hex_codec')))
        else:
          f.write('%s|%d|FALSE\n' % (record[0].encode('hex_codec'), record[1]))

    endtime = time.clock()
    print 'RUNTIME:', endtime - starttime
    
  print 'MAP FINISH'

if __name__ == '__main__':
  main()