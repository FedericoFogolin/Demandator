import sqlite3
import hashlib
import random
import logging
import verboselogs

'''

This is the module that Handels the access to the database.
It allows to open or create a database, add new users
and verify their existence.

Functions:
- open_or_create: connects to the database (creating it if
                  it doesn't exist) and creates the user table
- open_database: connects to the database and retrieves an
                 error if it doesn't exist
- check_for_username: verifies the existence of a user
- save_new_username: adds new username and password

'''

conn = None
cursor = None

logger = verboselogs.VerboseLogger('demo')
logger.addHandler(logging.StreamHandler())


def open_or_create(verbose, db_file):
    '''
    Function that creates the users' database and related table or
    opens it if it already exists.
    ----------
    Parameters
    ----------
    verbose : choose the verbosity level (type: int)
    db_file : set the location of your database (type: str)
    '''
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
    '''
    Open current users' database, return False if database doesn't exist
    ----------
    Parameters
    ----------
    verbose : choose the verbosity level (type: int)
    db_file : set the location of your database (type: str)
    '''
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
    except sqlite3.OperationalError:
        logger.error('''[ERROR] Cannot connect to the Database
                     user table. Please check its existence
                     or create a new one and add a new User''')
        return False


def check_for_username(username, password, verbose):
    """
    Check if current user is present in the users' database
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
        salt = cursor.execute("SELECT salt FROM user WHERE username=?",
                              [username]).fetchall()[0][0]
        conn.commit()
    except IndexError:
        conn.close()
        return False

    if salt:
        digest = salt + password

        for i in range(1000000):
            digest = hashlib.sha256(digest.encode('utf-8')).hexdigest()

        rows = cursor.execute('''SELECT * FROM user WHERE username=?
                              and password=?''', (username, digest))
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
            cursor.execute("INSERT OR REPLACE INTO user VALUES (?,?,?)",
                           (username, salt, digest))
            conn.commit()
        except:
            logger.error('''[ERROR] Something went wrong while adding
                         the new User''')
            conn.close()
            return
        conn.close()
        logger.success('''[SUCCESS] A new user has been added to the database.
                       Sign in with the new User.''')
        return