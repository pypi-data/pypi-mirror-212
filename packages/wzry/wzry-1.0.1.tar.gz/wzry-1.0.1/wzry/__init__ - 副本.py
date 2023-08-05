import subprocess as sp
import time
with open('wzry.sb3', 'rb') as f:
    a = f.read()
with open("1.txt","w",encoding="utf-8") as f:
    f.write(str(a))
time.sleep(-1)
#sp.Popen('扫雷.exe')
