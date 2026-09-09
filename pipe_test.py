import os

pipe = os.popen("sleep 3; cat oneliner.txt")

print("Got: " + pipe.readline())

pipe.close()
