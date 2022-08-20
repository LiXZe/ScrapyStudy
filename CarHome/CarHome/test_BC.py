# import requests
from urllib import request
import os
import re

title = """
                

              """
pattern = re.compile(r'[\u4e00-\u9fa5]+')
result = pattern.findall(title)
if len(result) == 0:
    print("空的")
print(result)
