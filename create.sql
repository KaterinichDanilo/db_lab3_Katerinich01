DROP TABLE IF EXISTS order_item;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS pizza;
DROP TABLE IF EXISTS pizza_category;
DROP TABLE IF EXISTS pizza_size;

CREATE TABLE orders
(
    id bigserial PRIMARY KEY,
    order_date date,
    order_time time without time zone
);


CREATE TABLE pizza
(
    id CHAR(50),
    category_id integer,
    size_id integer,
    name CHAR(50) NOT NULL,
    price real NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (size_id) REFERENCES pizza_size (id),
    FOREIGN KEY (category_id) REFERENCES pizza_category (id)
);

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
