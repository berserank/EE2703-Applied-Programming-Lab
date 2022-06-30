from asyncio import DatagramProtocol
from sys import argv, exit
f = open("faggot.txt")
data = f.read()
f.close()
print(data)