import requests
import ast

def demandator (path, verbose, n_results):
    url = 'https://fishidtest.herokuapp.com/api/test'
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
    results = ast.literal_eval((r.content).decode("utf-8"))['results']
    for count, i in enumerate (results):
        result = i.split(',')
	# solve string result if value is == 1.0 (really remote case)
        print ('Result n.{} label:{} probability: {}'.format(result[0], result[1], result[2]))
        # stop iterations on the based on number of results asked 
        # (count + 1) because enumerate starts from 0
        if (count+1) == n_results:
            break
