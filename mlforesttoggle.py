#!/usr/bin/python

import argparse
import subprocess

parser = argparse.ArgumentParser()

parser.add_argument("-t", "--trg", help="target host")
parser.add_argument("-s", "--src", help="source database")
parser.add_argument("-d", "--dst", help="destination database")
parser.add_argument("-u", "--usr", help="user")
parser.add_argument("-p", "--pas", help="password")
args = parser.parse_args()

DB1GetConfig="curl -s -X GET --anyauth -u {}:{} http://{}:8002/manage/v2/databases/{}/properties ".format((args.usr), (args.pas), (args.trg), (args.src))
DB1xml=subprocess.Popen(DB1GetConfig.split(" "),stdout=subprocess.PIPE)
DB1=DB1xml.stdout.read()
DB1Forests=[]
for line in DB1.splitlines():
  if "<forest>" in line:
    line = line.translate(None, ' ')
    DB1Forests.append(line[8:-9])
print DB1Forests

DB2GetConfig="curl -s -X GET --anyauth -u {}:{} http://{}:8002/manage/v2/databases/{}/properties ".format((args.usr), (args.pas), (args.trg), (args.dst))
DB2xml=subprocess.Popen(DB2GetConfig.split(" "),stdout=subprocess.PIPE)
DB2=DB2xml.stdout.read()
DB2Forests=[]
for line in DB2.splitlines():
  if "<forest>" in line:
    line = line.translate(None, ' ')
    DB2Forests.append(line[8:-9])
print DB2Forests

for forest in DB1Forests:
  DB1ForestDetach="curl -s --anyauth -u {}:{} -X POST -i -d state=detach -d database={} -H Content-type:application/x-www-form-urlencoded http://{}:8002/manage/v2/forests/{}".format((args.usr), (args.pas), (args.src), (args.trg), (forest))
  print(DB1ForestDetach)
  subprocess.call(DB1ForestDetach.split(" "))

for forest in DB2Forests:
  DB2ForestDetach="curl -s --anyauth -u {}:{} -X POST -i -d state=detach -d database={} -H Content-type:application/x-www-form-urlencoded http://{}:8002/manage/v2/forests/{}".format((args.usr), (args.pas), (args.dst), (args.trg), (forest))
  print(DB2ForestDetach)
  subprocess.call(DB2ForestDetach.split(" "))

for forest in DB1Forests:
  DB1ForestAttach="curl -s --anyauth -u {}:{} -X POST -i -d state=attach -d database={} -H Content-type:application/x-www-form-urlencoded http://{}:8002/manage/v2/forests/{}".format((args.usr), (args.pas), (args.dst), (args.trg), (forest))
  print(DB1ForestAttach)
  subprocess.call(DB1ForestAttach.split(" "))

for forest in DB2Forests:
  DB2ForestAttach="curl -s --anyauth -u {}:{} -X POST -i -d state=attach -d database={} -H Content-type:application/x-www-form-urlencoded http://{}:8002/manage/v2/forests/{}".format((args.usr), (args.pas), (args.src), (args.trg), (forest))
  print(DB2ForestAttach)
  subprocess.call(DB2ForestAttach.split(" "))


