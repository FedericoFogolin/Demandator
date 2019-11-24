import requests

def demandator (path, verbose):
    url = 'https://fishidtest.herokuapp.com/api/test'
    files = {'file_field': open(path, 'rb')}
    
    if verbose >= 2:
        print('Getting the image from the path  :  ' + path)
        print('Sending the image to the API at  :  ' + url)
    elif verbose == 1:
        print('Sending the image ...')
    
    r = requests.post(url, files=files)
    if verbose >= 1:
        print('Getting the results ...')
    
    print(r.content)