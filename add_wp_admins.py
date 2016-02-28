## Checks every MySQL database on a server, finds the wordpress ones, and adds an admin user to each one
## I used this on an infected server to quickly get admin access to all the infected sites so I could
## add some WordPress anti-virus plugins that were catching stuff I couldn't see.  

## TODO: tighten this up, put into functions, get it to auto-install the WP plugins,
## save csv or something to delete the added users,
## enable logging, put into modular classes, add xtra cheese and more cowbell.

import MySQLdb
import re
import logging

MySQLuser = "newroot"
MySQLpasswd = "passw0rd"
adminuser = "virushunter"
adminpass = "passw0rd"
admin_nicename = "guydude"
admin_email = "not@real.com"
admin_url = "http://www.nope.com"
admin_status = '0'
admin_displayname = "Guy Dude"


db = MySQLdb.connect(user=MySQLuser, passwd=MySQLpasswd)
c = db.cursor()

# Retrieve Databases
c.execute("SHOW DATABASES;")
databasesRAW = c.fetchall()
database_list = [y for x in databasesRAW for y in x]

# Begin populating table data into database dictionary
db_dict = {}
for db in database_list:
        cmd = "SHOW TABLES FROM %s" % (db)
        c.execute(cmd)
        tablesRAW = c.fetchall()
        tables = [y for x in tablesRAW for y in x]
        db_dict[db] = tables

# Filter out databases that aren't WordPress
# TODO: find better match criteria. Crawl home directories and match usernames to dbs from 
# wp-config.php
wponly_DBdict = {}
# Can I do this all in one line?
# wponly_DBdict = {db:db_dict[db] for db in db_dict if any(v.endswith("_users") for v in db.values())}

for db, tables in db_dict.iteritems():
    for table in tables:
        if "_users" in table:
            print "DB %s is a wordpress database" % (db)
            # If using python 2.6.6 or lower:
            wponly_DBdict[db] = tables
            break
        else:
            db_dict[db] = "deleted"
    # dictionary comprehensions don't work in python 2.6.6 :-\
    # wponly_DBdict = {db:db_dict[db] for db in db_dict if db_dict[db] != "deleted"}

# Go through WP MySQL databases and add a user with admin privledges to each one
for db, tables in wponly_DBdict.iteritems():
    # figure out pertinent information in case of funny prefixes:
    wp_users = [table for table in tables if table.endswith("_users")][0]
    wp_usermeta = [table for table in tables if table.endswith("_usermeta")][0]
    # sets the userID to current max ID plus 1000
    cmd = "SELECT max(ID) FROM %s.%s" % (db, wp_users)
    c.execute(cmd)
    userID = int(c.fetchall()[0][0]) + 1000
    # Insert the new admin user:
    cmd = """INSERT INTO \'%s\'.\'%s\' (\'ID\', \'user_login\', \'user_pass\',\
    \'user_nicename\', \'user_email\', \'user_status\')\
    VALUES\
    (\'%d\', MD5(\'%s\'), \'%s\', \'%s\', \'%s\');""" % (db, wp_users,
        userID, adminuser, adminpass, admin_nicename, admin_email, admin_status)
    c.execute(cmd)
    cmd = """INSERT INTO \'%s\'.\'%s\', (\'user_id\', \'meta_key\', \'meta_value\')\
    VALUES\
    (\'%d\', \'wp_capabilities\', \'a:1:{s:13:\"administrator\";b:1;}\');""" % (
        db, wp_usermeta, userID)
    c.execute(cmd)
    cmd = """INSERT INTO \'%s\',\'%s\' (\'user_id\', \'meta_key\', \'meta_value\')\
    VALUES\
    (\'%d\', \'wp_user_level\', \'10\');""" % (db, wp_usermeta, userID)
    c.execute(cmd)

print "Admin user %s added to databases." % (adminuser)
c.close()









