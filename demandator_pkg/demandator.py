import requests

def demandator (path, verbose):
    url = 'https://fishidtest.herokuapp.com/api/test'
    print(path)
    try:
        files = {'file_field': open(path, 'rb')}
    except FileNotFoundError:
        print('[ERROR] File not found. Make sure the path is correct and the file is available.')
        return 
    if verbose >= 2:
        print('[INFO] Getting the image from the path  :  ' + path)
        print('[INFO] Sending the image to the API at  :  ' + url)
    elif verbose == 1:
        print('[INFO] Sending the image ...')
    
    r = requests.post(url, files=files)
    if verbose >= 1:
        print('[INFO] Getting the results ...')
    
    print(r.content)
