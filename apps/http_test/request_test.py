
import requests
ret = requests.get('http://127.0.0.1:5000/test')

with open('/root/dfp.tar.gz', 'wb') as fp:
    fp.write(ret.content)
