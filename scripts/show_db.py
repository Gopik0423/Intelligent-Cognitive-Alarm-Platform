import sqlite3, json
c = sqlite3.connect('test.db')
cur = c.cursor()
cur.execute("SELECT id,user_id,challenge_type,attempts,accuracy,success,completion_time,completed_at FROM performance_logs")
rows = cur.fetchall()
cols = [d[0] for d in cur.description]
print(json.dumps([dict(zip(cols, r)) for r in rows], default=str, indent=2))
