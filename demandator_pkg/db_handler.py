import sqlite3
import hashlib
import random
import logging
import verboselogs

conn = None
cursor = None

logger = verboselogs.VerboseLogger('demo')
logger.addHandler(logging.StreamHandler())


def open_or_create(verbose, db_file):
    """
    Function to create users database or open it if already exist
    """
    if verbose >= 2:
        logger.setLevel(logging.SPAM)
    elif verbose == 1:
        logger.setLevel(logging.VERBOSE)
    elif verbose == 0:
        logger.setLevel(logging.ERROR)

    global conn
    global cursor
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    logger.verbose('[INFO] Connecting to the DataBase')
    try:
        cursor.execute("SELECT * FROM user")
    except sqlite3.OperationalError:
        # Create table
        cursor.execute('''CREATE TABLE user
                     (username CHAR(256) NOT NULL,
                     salt CHAR(256) NOT NULL,
                     password CHAR(256) NOT NULL,
                     PRIMARY KEY (username))''')


def open_database(verbose, db_file):
    """
    Open current user database, return False if database is not existent
    """
    if verbose >= 2:
        logger.setLevel(logging.SPAM)
    elif verbose == 1:
        logger.setLevel(logging.VERBOSE)
    elif verbose == 0:
        logger.setLevel(logging.ERROR)
    
    global conn
    global cursor
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    logger.verbose('[INFO] Connecting to the DataBase')
    try:
        cursor.execute("SELECT * FROM user")
        return True
    except:
        logger.error(
            '[ERROR] Cannot connect to the Database user table. Please check its existence or create a new one and '
            'add a new User')
        return False


def check_for_username(username, password, verbose):
    """
    Check if current user is present in the users database
    ----------
    Parameters
    ----------
    username : string
    password : string
    verbose : int
    """
    if verbose >= 2:
        logger.setLevel(logging.SPAM)
    elif verbose == 1:
        logger.setLevel(logging.VERBOSE)
    elif verbose == 0:
        logger.setLevel(logging.ERROR)
    global conn
    global cursor
    
    logger.spam('[INFO] Checking if user already exists')
    try:
        salt = cursor.execute("SELECT salt FROM user WHERE username=?", [username]).fetchall()[0][0]
        conn.commit()
    except:
        conn.close()
        return False

    if salt:
        digest = salt + password

        for i in range(1000000):
            digest = hashlib.sha256(digest.encode('utf-8')).hexdigest()

        rows = cursor.execute("SELECT * FROM user WHERE username=? and password=?", (username, digest))
        conn.commit()
        results = rows.fetchall()
        conn.close()
        return results


def save_new_username(username, password, verbose):
    """
    Check if user already exist, if not creates new user and psw
    ----------
    Parameters
    ----------
    username : string
    password : string
    verbose : int
    """
    if verbose >= 2:
        logger.setLevel(logging.SPAM)
    elif verbose == 1:
        logger.setLevel(logging.VERBOSE)
        logger.setLevel(logging.SUCCESS)
    elif verbose == 0:
        logger.setLevel(logging.ERROR)

    global conn
    global cursor
    logger.spam('Verifying if the Username and Password already exist...')

    rows = cursor.execute("SELECT * FROM user WHERE username=?", [username])
    conn.commit()
    if rows.fetchall():
        conn.close()
        logger.error("[ERROR] The user already exists, add a different one.")
        return
    else:
        logger.spam('You inserted a new user...')
        salt = str(random.random())
        digest = salt + password
        logger.spam('Generating your hashed password...')
        for i in range(1000000):
            digest = hashlib.sha256(digest.encode('utf-8')).hexdigest()
        try:
            cursor.execute("INSERT OR REPLACE INTO user VALUES (?,?,?)", (username, salt, digest))
            conn.commit()
        except:
            logger.error('[ERROR] Something went wrong while adding the new User')
            conn.close()
            return
        conn.close()
        logger.success('[SUCCESS] A new user has been added to the database. Sign in with the new User.')
        return
