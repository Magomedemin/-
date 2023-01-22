SELECT * FROM post;
SELECT * FROM employee;
SELECT * FROM "order";
SELECT * FROM ingredients;
SELECT * FROM coffee_drink;
SELECT * FROM coffee_ingredients;
SELECT * FROM position_order;
SELECT * FROM toppings;
SELECT * FROM toppings_in_order;

INSERT INTO employee (first_name, last_name, patronymic, birth_date, phone_number, post_id) VALUES
('Георгий', 'Плеханов', 'Валентинович', '1856-11-29', '+7(999) 999 99-99', 3);

INSERT INTO post (title, salary) VALUES
('Российский философ', '100000');

UPDATE post
SET salary = 150000
WHERE id = 4

UPDATE employee
SET phone_number = '+7(777) 777 77-77'
WHERE phone_number = '+7(999) 999 99-99'

DELETE FROM post
WHERE title = 'Российский философ'

DELETE FROM employee
WHERE birth_date = '1856-11-29'

SELECT SUM (sum_price) AS Сумма_всех_заказов FROM "order";

SELECT COUNT (id) AS Общее_количество_заказов FROM "order";

SELECT AVG (sum_price) AS Средний_чек FROM "order";

SELECT MIN (sum_price) AS Самый_дешевый_заказ FROM "order";

SELECT MAX (sum_price) AS Самый_дорогой_заказ FROM "order";

SELECT * FROM ingredients ORDER BY price ASC;

SELECT * FROM ingredients ORDER BY price DESC;

SELECT * FROM ingredients WHERE price < 100;

SELECT * FROM ingredients LIMIT 3;

SELECT * FROM ingredients OFFSET 3;

SELECT * FROM ingredients WHERE price > 300;

SELECT * FROM ingredients WHERE price >= 135;

SELECT * FROM ingredients WHERE price <= 125;

SELECT * FROM ingredients WHERE price = 7;

SELECT * FROM ingredients WHERE price != 7;

SELECT * FROM ingredients WHERE price <> 90;

SELECT * FROM ingredients WHERE price > 7 AND price < 135;

SELECT * FROM ingredients WHERE price = 7 OR price = 450;

SELECT * FROM ingredients WHERE description IN ('Чистая вода', 'Порошок молотого кофе арабики');

SELECT * FROM ingredients WHERE description NOT IN ('Чистая вода', 'Порошок молотого кофе арабики');

INSERT INTO post (title, salary) VALUES
('Российский философ', '100000');

UPDATE post
SET salary = 80000
WHERE id = 5

SELECT * FROM post;

SELECT DISTINCT salary AS Уникальные_зп FROM post;

SELECT * FROM post WHERE title LIKE '_ари%';

SELECT * FROM post WHERE title SIMILAR TO '%с{2}%';

SELECT e.first_name AS Имя_сотрудника, e.last_name AS Фамилия_сотрудника, p.title AS Должность
FROM employee e INNER JOIN post p ON p.id = e.id;

SELECT e.first_name AS Имя_сотрудника, e.last_name AS Фамилия_сотрудника, p.title AS Должность
FROM employee e RIGHT JOIN post p ON p.id = e.id;

ALTER TABLE employee
ALTER COLUMN post_id DROP NOT NULL;

INSERT INTO employee (first_name, last_name, patronymic, birth_date, phone_number) VALUES
('Георгий', 'Плеханов', 'Валентинович', '1856-11-29', '+7(999) 999 99-99');

SELECT e.first_name AS Имя_сотрудника, e.last_name AS Фамилия_сотрудника, p.title AS Должность
FROM employee e LEFT JOIN post p ON p.id = e.id;

--Удалил NOT NULL чтобы убрать обязательность поля «Должность» и была видна разница в LEFT JOIN,
--иначе он дублировал INNER JOIN

SELECT * FROM ingredients WHERE price > (SELECT AVG (price) FROM ingredients);

CREATE VIEW Sum_price_orders AS SELECT SUM (sum_price) AS Сумма_всех_заказов FROM "order";
SELECT * FROM Sum_price_orders;

SELECT * FROM coffee_drink;

BEGIN;

UPDATE coffee_drink SET price = price - 10 WHERE id = 1;
UPDATE coffee_drink SET price = price + 10 WHERE id = 2;

COMMIT;
