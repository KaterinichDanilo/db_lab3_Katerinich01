import json
import psycopg2

username = 'postgres'
password = '0000'
database = 'Lab_DB'
host = 'localhost'
port = '5432'

conn = psycopg2.connect(user=username, password=password, dbname=database)

data = {}
with conn:
    cur = conn.cursor()

    for table in ('pizza', 'orders', 'order_item'):
        cur.execute('SELECT * FROM ' + table)
        rows = []
        fields = [x[0] for x in cur.description]

        for row in cur:
            rows.append(dict(zip(fields, row)))

        data[table] = rows

with open('all_data.json', 'w') as outf:
    json.dump(data, outf, default=str)