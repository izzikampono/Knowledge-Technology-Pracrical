import json
import numpy as np

f=open('kb.json')
facts = json.load(f)
for i in facts:
    print(i)

f.close()
    