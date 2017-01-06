from __future__ import with_statement, print_function
import sys
import urllib2
import json
import hashlib


keyword = ' '.join(sys.argv[1:])
url = 'http://mobilecdn.kugou.com/api/v3/search/song?format=json&page=1&pagesize=20&keyword=%27{0}%27'.format(keyword)

request = urllib2.Request(url)
response = urllib2.urlopen(request).read()
data = json.loads(response)

if len(data['data']['info']) > 0:
	print('Found the following songs, which one do you want?')
else:
	print('Couldn\'t find anything for', keyword)
	sys.exit()

count = 0
for songInfo in data['data']['info']:
	filename = songInfo['filename']
	optionString = u'[{0}] {1}'.format(count, filename)
	if len(songInfo['320hash']) > 0:
		optionString += ' 320kbps'
	print(optionString)
	count = count + 1

optionSelected = input()
songHash = data['data']['info'][optionSelected]['320hash'] if len(data['data']['info'][optionSelected]['320hash']) else data['data']['info'][optionSelected]['hash']

m = hashlib.md5()
m.update(songHash + 'kgcloud')
MD5Hash = m.hexdigest()

url = 'http://trackercdn.kugou.com/i/?cmd=4&hash={0}&key={1}&pid=1&forceDown=0&vip=1'.format(songHash, MD5Hash)

request = urllib2.Request(url)
response = urllib2.urlopen(request).read()
data = json.loads(response)

filename = data['fileName']+'.mp3'
mp3url = data['url']
mp3file = urllib2.urlopen(mp3url)

print('downloading...')
with open(filename,'wb') as output:
    while True:
        buf = mp3file.read(65536)
        if not buf:
            break
        output.write(buf)
        print('.', end="")
        sys.stdout.flush()

print('done!')