import os

dmy = os.popen(r"grep 'version=\".*\"' setup.py").read()
print(int(dmy.split(".")[-1].split("\"")[0]))