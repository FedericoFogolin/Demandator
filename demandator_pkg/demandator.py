import demandator_pkg.plotter as plt
import requests
import ast
import sqlite3
import hashlib
from PIL import Image
import cv2
import logging
import verboselogs


def demandator(path, verbose, n_results, threshold, plot):
    '''It takes an image and returns through an API its
       classification with the related probability
       of being classified correctly.
    ----------
    Parameters
    ----------
    path : string
        path of the image to analyze
    verbose : int
        level of verbosity of the function
    n_results : int
        number of results desired to show
    threshold : float
        minimum level of classification probability
    plot : bool
        enable plotting of results
    '''
    logger = verboselogs.VerboseLogger('demo')
    logger.addHandler(logging.StreamHandler())

    if verbose >= 2:
        logger.setLevel(logging.SPAM)
    elif verbose == 1:
        logger.setLevel(logging.VERBOSE)
    elif verbose == 0:
        logger.setLevel(logging.WARNING)

    url = 'https://fishidtest.herokuapp.com/api/test'
    conn = sqlite3.connect('db_images.db')
    cursor = conn.cursor()
    try:
        files = {'file_field': open(path, 'rb')}
        # check if file is image
        logger.spam('[INFO] Checking image')
        Image.open(path)
        cv2.imread(path)
    except FileNotFoundError:
        logger.error('''[ERROR] File not found. Make sure the
                     path is correct and the file is available.''')
        exit()
    except IOError:
        logger.error('[ERROR] The file is not an image.')
        exit()
    except:
        logger.error('[ERROR] Error with reading the file.')

    logger.spam('[INFO] Getting the image from the path:  ' + path)
    logger.spam('[INFO] Sending the image to the API at:  ' + url)

    try:
        r = requests.post(url, files=files)
    except requests.exceptions.ConnectionError:
        logger.error('''[ERROR] Cannot connect to the server.
                     Please verify your connection.''')
        return

    logger.verbose('[INFO] Getting the results')

    results = ast.literal_eval((r.content).decode("utf-8"))['results']
    if 'Error' in ast.literal_eval((r.content).decode("utf-8")):
        logger.error('''[ERROR] Error in the image. The error will be
                     displayed in the next line.''')
        logger.error('[ERROR] Error: {}').format(ast.literal_eval((r.content).decode("utf-8"))['Error'])
        exit()

    data = []
    for count, i in enumerate(results):
        result = i.split(',')
        # initiate the database and insert values in it
        # do it for first result on database
        if count == 0:
            accuracy = float(result[2])
            blobim = convert_to_binary_data(path)
            imhash = hashlib.sha256(blobim).hexdigest()
            logger.spam('[INFO] Saving the best result in our database')

            try:
                cursor.execute("SELECT * FROM images")
            except sqlite3.OperationalError:
                cursor.execute('''CREATE TABLE images(image_hash TEXT NOT NULL,
                               image_blob BLOB NOT NULL, prediction_accuracy
                               REAL NOT NULL, PRIMARY KEY (image_hash))''')
            finally:
                if len(cursor.execute('''SELECT * FROM images WHERE
                                      image_hash=?''',
                       [imhash]).fetchall()) == 1:
                    cursor.execute('''INSERT INTO images (image_hash,
                                   image_blob, prediction_accuracy)
                                   VALUES (?,?,?)''',
                                   (imhash, blobim, accuracy))
                    conn.commit()

        # TODO solve string result if value is == 1.0 (really remote case)
        # check that prediction has accuracy >= of threshold
        # (that is 0.0 as default)
        if float(result[2]) >= threshold:
            data.append((result[1], int(float(result[2]) * 100)))
            if not plot:
                print('{}: {:.1%}'.format(result[1], float(result[2])))
        elif float(result[2]) < threshold:
            if count == 0:
                print('''[INFO] No prediction found, try to lower the
                      accuracy threshold with the parameter -t ''')
                exit()
            break
        # stop iterations on the based on number of results asked
        # (count + 1) because enumerate starts from 0
        if (count + 1) == n_results:
            break
    if plot:
        logger.spam('[INFO] preparing the graph.')
        plt.plotting(data)


def convert_to_binary_data(path):
    with open(path, 'rb') as file:
        blobim = file.read()
    return blobim
