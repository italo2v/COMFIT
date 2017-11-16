import sys
from TOSSIM import *
t = Tossim([])
m = t.getNode(5)
m.bootAtTime(45654)
t.addChannel("Boot", sys.stdout)
t.runNextEvent()
f = open("log.txt", "w")
t.addChannel("BlinkC", f)
#while (m.isOn()):
for i in range(0, 100):
    t.runNextEvent()
    
