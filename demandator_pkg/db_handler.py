import sqlite3
import hashlib
import random
import logging
import verboselogs

conn = None
cursor = None

logger = verboselogs.VerboseLogger('demo')
logger.addHandler(logging.StreamHandler())

def open_or_create(verbose):
    if verbose >= 2:
        logger.setLevel(logging.SPAM)
    elif verbose == 1:
        logger.setLevel(logging.VERBOSE)
    elif verbose == 0:
        logger.setLevel(logging.WARNING)
    
    global conn
    global cursor
    conn = sqlite3.connect('./user-pwd.db')
    cursor = conn.cursor()
    logger.spam('Connecting to database...')
    try:
        cursor.execute("SELECT * FROM user")
    except sqlite3.OperationalError:
        # Create table
        cursor.execute('''CREATE TABLE user
                     (username CHAR(256) NOT NULL,
                     salt CHAR(256) NOT NULL,
                     password CHAR(256) NOT NULL,
                     PRIMARY KEY (username))''')

def open_database():
    global conn
    global cursor
    conn = sqlite3.connect('user-pwd.db')
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM user")
    except:
        logger.error('[ERROR] Cannot connect to the Database. Please check its existence or create a new one and add a new User')


def check_for_username (username, password, verbose):
    if verbose >= 2:
        logger.setLevel(logging.SPAM)
    elif verbose == 1:
        logger.setLevel(logging.VERBOSE)
    elif verbose == 0:
        logger.setLevel(logging.WARNING)
    global conn
    global cursor
    
    logger.spam('Checking if user already exists...')
    try:
        salt = cursor.execute("SELECT salt FROM user WHERE username=?", [username]).fetchall()[0][0]
        conn.commit()
    except:
        logger.error('[ERROR] Username is not present or password is invalid.')
        conn.close()
        return
    
    if salt:
        digest = salt + password
        
        for i in range(1000000):
            digest = hashlib.sha256(digest.encode('utf-8')).hexdigest()
        
        rows = cursor.execute("SELECT * FROM user WHERE username=? and password=?", (username, digest))
        #conn.commit()
        results = rows.fetchall()
        conn.close()
        return results
    

def save_new_username(username, password):
    global conn
    global cursor
    
    rows = cursor.execute("SELECT * FROM user WHERE username=?",[username])
    conn.commit()
    if rows.fetchall():
        conn.close()
        logger.error("[ERROR] The user already exists, add a different one.")
        return
    else:
        salt = str(random.random())
        digest = salt + password
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
        logger.error('[SUCCESS] A new user has been added to the database. Sign in with the new User.')
        return
