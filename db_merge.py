import sys
import sqlite3

old_db = sys.argv[1]
new_db = sys.argv[2]

try:
    con_old = sqlite3.connect(old_db)
    cur_old = con_old.cursor()
    old_users = cur_old.execute('select * from users').fetchall()
    old_bookmarks = cur_old.execute('select * from bookmarks').fetchall()
    old_feeds = cur_old.execute('select * from feeds').fetchall()
except sqlite3.Error, e:
    print("Error %s:" % e.args[0])
    exit()

try:
    con_new = sqlite3.connect(new_db)
    cur_new = con_new.cursor()
except sqlite3.Error, e:
    print("Error %s:" % e.args[0])
    exit()

for u in old_users:
    print(u)
    cur_new.execute("insert into users (id, username, email, password, last_logged, per_page, suggestion, recently) values (?,?,?,?,?,?,?,?)",
                    (u[0], u[1], u[2], u[3], u[4], u[5], u[7], u[6]))
    con_new.commit()

for b in old_bookmarks:
    print(b)
    cur_new.execute("insert into marks (owner_id, type, title, url, tags, clicks, last_clicked, created, updated) values (?,?,?,?,?,?,?,?,?)",
                    (b[1], 'bookmark', b[2], b[3], b[4], b[5], b[8], b[6], b[7]))
    con_new.commit()

for f in old_feeds:
    print(f)
    cur_new.execute("insert into marks (owner_id, type, title, url, tags, clicks, last_clicked, created, updated) values (?,?,?,?,?,?,?,?,?)",
                    (f[1], 'feed', f[2], f[3], f[4], f[5], f[6], f[7], f[8]))
    con_new.commit()

con_new.close()
con_old.close()
