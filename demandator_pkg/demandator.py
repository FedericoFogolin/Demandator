import requests
import ast

def demandator (path, verbose, n_results, threshold):
    url = 'https://fishidtest.herokuapp.com/api/test'
    try:
        files = {'file_field': open(path, 'rb')}
    except FileNotFoundError:
        print('[ERROR] File not found. Make sure the path is correct and the file is available.')
        return
    
    # to remove and substitute with logging module
    if verbose >= 2:
        print('[INFO] Getting the image from the path  :  ' + path)
        print('[INFO] Sending the image to the API at  :  ' + url)
    elif verbose == 1:
        print('[INFO] Sending the image ...')
    # till here
    
    r = requests.post(url, files=files)
    
    # to remove and substitute with logging module
    if verbose >= 1:
        print('[INFO] Getting the results ...')
    # till here
    
    results = ast.literal_eval((r.content).decode("utf-8"))['results']
    for count, i in enumerate (results):
        result = i.split(',')
	# TODO solve string result if value is == 1.0 (really remote case)
        # check that prediction has accuracy >= of threshold (that is 0.0 as default)
        if float(result[2]) >= threshold:
            print('{}: {:.1%}'.format(result[1], float(result[2])))
        elif float(result[2]) < threshold:
            break
        # stop iterations on the based on number of results asked
        # (count + 1) because enumerate starts from 0
        if (count+1) == n_results:
            break
