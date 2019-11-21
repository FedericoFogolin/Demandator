import requests

def demandator (path):
    url = 'https://fishidtest.herokuapp.com/api/test'
    files = {'file_field': open(path, 'rb')}
    r = requests.post(url, files=files)
    print(r.content)

