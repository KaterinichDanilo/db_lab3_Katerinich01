DROP TABLE IF EXISTS orderscopy; 
create table orderscopy as select * from orders; 
delete from orderscopy;

DO $$
 DECLARE
     order_id   orderscopy.id%TYPE;
     order_date orderscopy.order_date%TYPE;
	 order_time orderscopy.order_time%TYPE;

 BEGIN
     order_id := 0;
     FOR counter IN 1..10
         LOOP
            INSERT INTO orderscopy (id, order_date, order_time)
             VALUES (counter + order_id, current_date - counter + 1, CURRENT_TIME);
         END LOOP;
 END;
 $$