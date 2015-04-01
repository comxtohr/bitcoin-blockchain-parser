##Feature
- get top 100 richest bitcoin accounts' address
- MapReduce

##Usage
- `python map.py #1 #2` - run map on blk#1.dat ~ blk#2.dat, output mapPair#1.txt ~ mapPair#2.txt in `./mapPair/`
- `python reduce.py #1 #2` - run reduce on mapPair#1.txt ~ mapPair#2.txt, output reducePair#1-#2.txt in `./reducePair/`
- `python reduce^2.py #1 #2 #3 #4` - run reduce^2 on reducePair#1-#2.txt & reducePair#3-#4.txt, output reducePair#1-#4.txt in `./reduce^2Pair/`
- `python reduce^3.py #1 #2 #3 #4` - run reduce^3 on reducePair#1-#2.txt & reducePair#3-#4.txt, output reducePair#1-#4.txt in `./reduce^3Pair/`
