import requests
import ast
from termgraph import termgraph as tg
import terminalplot as tp
import numpy as np
from math import sin, pi


def demandator (path, verbose, n_results, threshold, plot):
    url = 'https://fishidtest.herokuapp.com/api/test'
    global conn
    global cursor
    conn = sqlite3.connect('db_images.db')
    cursor = conn.cursor()

    def convert_to_binary_data(path):
        with open(path, 'rb') as file:
            blobim = file.read()
        return blobim

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
        #initiate the database and insert values in it
        if count == 0:
            accuracy = float(result[2])
            blobim = convert_to_binary_data(path)
            imhash = hashlib.sha256(blobim).hexdigest()

            try:
                cursor.execute("SELECT * FROM images")
            except sqlite3.OperationalError:
                cursor.execute('''CREATE TABLE images(image_hash TEXT NOT NULL, image_blob BLOB NOT NULL, prediction_accuracy REAL NOT NULL, PRIMARY KEY (imahe_hash))''')
            finally:
                if len(cursor.execute("SELECT * FROM images WHERE image_hash=?", [imhash]).fetchall()) == 1:
                    cursor.execute("INSERT INTO images (image_hash, image_blob, prediction_accuracy) VALUES (?,?,?)", (imhash, blobim, accuracy))
                    conn.commit()

	# TODO solve string result if value is == 1.0 (really remote case)
        # check that prediction has accuracy >= of threshold (that is 0.0 as default)
        if float(result[2]) >= threshold:
            data.append((result[1], int(float(result[2])*100)))
            if plot != True:
                print('{}: {:.1%}'.format(result[1], float(result[2])))
        elif float(result[2]) < threshold:
            if count == 0:
                print('[INFO] No prediction found, try to lower the accuracy treshold with the parameter -t ')
                exit()
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

