import psycopg2
import matplotlib.pyplot as plt

username = 'postgres'
password = '0000'
database = 'Lab_DB'
host = 'localhost'
port = '5432'

query_1 = '''
create view QuantityPizzaInOrders as
SELECT orders.id, SUM(order_item.quantity)
FROM orders
LEFT JOIN order_item ON order_item.order_id = orders.id
GROUP BY orders.id
ORDER BY orders.id;
'''

query_2 = '''
create view QuantityPizza as
SELECT TRIM(pizza.id), SUM(order_item.quantity)
FROM pizza
LEFT JOIN order_item ON order_item.pizza_id = pizza.id
GROUP BY pizza.id
ORDER BY pizza.id;
'''

query_3 = '''
create view PriceEachOrder as
SELECT orders.id, SUM(order_item.quantity*pizza.price) 
FROM orders
LEFT JOIN order_item ON order_item.order_id = orders.id
LEFT JOIN pizza ON order_item.pizza_id = pizza.id
GROUP BY orders.id
ORDER BY orders.id;
'''



conn = psycopg2.connect(user=username, password=password, dbname=database, host=host, port=port)

with conn:
    cur = conn.cursor()
    cur.execute('DROP VIEW IF EXISTS QuantityPizzaInOrders')
    cur.execute(query_1)
    cur.execute('SELECT * FROM QuantityPizzaInOrders')
    customers = []
    total = []
    for row in cur:
        customers.append(row[0])
        total.append(row[1])
    x_range = range(len(customers))

    figure, (bar_ax, pie_ax, graph_ax) = plt.subplots(1, 3)
    bar = bar_ax.bar(x_range, total, label='Total')
    bar_ax.set_xlabel('Замовлення')
    bar_ax.set_ylabel('Кількість')
    bar_ax.set_xticks(x_range)
    bar_ax.set_xticklabels(customers)

    cur.execute('DROP VIEW IF EXISTS QuantityPizza')
    cur.execute(query_2)

    cur.execute('SELECT * FROM QuantityPizza')
    item_name = []
    item_quantity = []

    for row in cur:
        item_name.append(row[0])
        item_quantity.append(row[1])

    pie_ax.pie(item_quantity, labels=item_name, autopct='%1.1f%%')
    pie_ax.set_title('Частка замовлень кожної піци')

    cur.execute('DROP VIEW IF EXISTS PriceEachOrder')
    cur.execute(query_3)

    cur.execute('SELECT * FROM PriceEachOrder')
    order_id = []
    order_price = []

    for row in cur:
        order_id.append(row[0])
        order_price.append(row[1])

    graph_ax.plot(order_id, order_price, marker='o')
    graph_ax.set_xlabel('Номер замовлення')
    graph_ax.set_ylabel('Ціна, $')
    graph_ax.set_title('Графік залежності ціни від замовлення')


    for qnt, price in zip(order_id, order_price):
        graph_ax.annotate(price, xy=(qnt, price), xytext=(7, 2), textcoords='offset points')

    mng = plt.get_current_fig_manager()
    mng.resize(1400, 600)
    plt.show()