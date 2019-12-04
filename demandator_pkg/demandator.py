import requests
import ast
from termgraph import termgraph as tg
import terminalplot as tp
import numpy as np
from math import sin, pi


def demandator (path, verbose, n_results, threshold, plot):
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
    data = []
    for count, i in enumerate (results):
        result = i.split(',')
	# TODO solve string result if value is == 1.0 (really remote case)
        # check that prediction has accuracy >= of threshold (that is 0.0 as default)
        if float(result[2]) >= threshold:
            data.append((result[1], int(float(result[2])*100)))
            if plot != True:
                print('{}: {:.1%}'.format(result[1], float(result[2])))
        elif float(result[2]) < threshold:
            break
        # stop iterations on the based on number of results asked
        # (count + 1) because enumerate starts from 0
        if (count+1) == n_results:
            break
    if plot:
        plotting(data)
    
    
    
    
    
# function to plot graphs in terminal gived data
# data kind: [(string, value), (string, value),,,]
def plotting(data):
    max_value = max(count for _, count in data)
    increment = max_value / 25
    longest_label_length = max(len(label) for label, _ in data)
    for label, count in data:

        # The ASCII block elements come in chunks of 8, so we work out how
        # many fractions of 8 we need.
        # https://en.wikipedia.org/wiki/Block_Elements
        bar_chunks, remainder = divmod(int(count * 8 / increment), 8)

        # First draw the full width chunks
        bar = '█' * bar_chunks

        # Then add the fractional part.  The Unicode code points for
        # block elements are (8/8), (7/8), (6/8), ... , so we need to
        # work backwards.
        if remainder > 0:
            bar += chr(ord('█') + (8 - remainder))

        # If the bar is empty, add a left one-eighth block
        bar = bar or  '▏'
        print(f'{label.rjust(longest_label_length)} ▏ {count:#4d}% {bar}')

