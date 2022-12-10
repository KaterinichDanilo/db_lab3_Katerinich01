import csv
import decimal
import psycopg2

username = 'postgres'
password = '0000'
database = 'Lab_DB'
host = 'localhost'
port = '5432'

INPUT_CSV_FILE = 'Data-Model-Pizza-Sales.csv'

query_createPizzaTable = '''
CREATE TABLE pizza
(
    id CHAR(50),
    category CHAR(50),
    pizza_size CHAR(50),
    pizza_name CHAR(50) NOT NULL,
    price real NOT NULL,
    PRIMARY KEY (id)
);

'''

query_createOrderTable = '''
CREATE TABLE orders
(
    id bigserial PRIMARY KEY,
    order_date date default current_date,
    order_time time without time zone
);
'''


query_createOrderItemTable = '''
CREATE TABLE order_item
(
    id bigserial,
    order_id integer NOT NULL,
    pizza_id CHAR(50) NOT NULL,
    quantity integer NOT NULL DEFAULT 1,
    PRIMARY KEY (id),
    FOREIGN KEY (order_id) REFERENCES public.orders (id),
    FOREIGN KEY (pizza_id) REFERENCES pizza (id)
);
'''

query_dropAlTables = '''
DROP TABLE IF EXISTS order_item;
DROP TABLE IF EXISTS pizza;
DROP TABLE IF EXISTS orders;
'''

query_insertPizza = '''
INSERT INTO pizza (id, category, pizza_size, pizza_name, price) VALUES (%s, %s, %s, %s, %s);
'''

query_insertOrder = '''
INSERT INTO orders (order_date, order_time) VALUES (%s, %s);
'''

query_insertOrderItem = '''
INSERT INTO order_item (order_id, pizza_id, quantity) VALUES (%s, %s, %s);
'''

query_getPizzaId = '''
SELECT id FROM pizza WHERE id = %s;
'''

query_getOrderId = '''
SELECT id FROM orders WHERE id = %s;
'''

conn = psycopg2.connect(user=username, password=password, dbname=database)

with conn:
    cur = conn.cursor()
    cur.execute(query_dropAlTables)
    cur.execute(query_createPizzaTable)
    cur.execute(query_createOrderTable)
    cur.execute(query_createOrderItemTable)

    with open(INPUT_CSV_FILE, 'r') as inf:
        reader = csv.DictReader(inf)
        for idx, row in enumerate(reader):
            pizzaId = row['pizza_id'];
            cur.execute(query_getPizzaId, (str(pizzaId),));
            list_id = cur.fetchone();
            if list_id is None:
                price = decimal.Decimal(row['unit_price'].lstrip('$'));
                values = (pizzaId, row['pizza_category'], row['pizza_size'], row['pizza_name'], price);
                cur.execute(query_insertPizza, values);

            orderId = row['order_id'];
            cur.execute(query_getOrderId, (int(orderId),));
            if cur.fetchone() is None:
                values = (row['order_date'], row['order_time']);
                cur.execute(query_insertOrder, values);

            values = (row['order_id'], row['pizza_id'], row['quantity']);
            cur.execute(query_insertOrderItem, values);

    conn.commit()