import urllib.request
import urllib.parse
import gzip
header = {
    'Host': 'tenhou.net',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0', 
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive'
}
req = urllib.request.Request(url="http://e3.mjv.jp/0/log/?2013010100gm-00e1-0000-e5440138", headers=header)
opener = urllib.request.build_opener()
response = opener.open(req)
response = gzip.decompress(response.read()).decode('utf-8')
print(response)
