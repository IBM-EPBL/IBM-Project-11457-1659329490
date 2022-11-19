CREATE TABLE IF NOT EXISTS users (
	id	INTEGER PRIMARY KEY,
	email TEXT NOT NULL,
	username	TEXT NOT NULL,
	password_hash	TEXT NOT NULL,
	income	REAL NOT NULL DEFAULT 60000.00,
	register_date	TEXT NOT NULL,
	last_login	TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS budgets (
	id	INTEGER PRIMARY KEY,
	name TEXT NOT NULL,
	amount	REAL,
	year TEXT,
	user_id	INTEGER NOT NULL,
	CONSTRAINT budgets_user_id_fkey FOREIGN KEY (user_id)
		REFERENCES users (id) 
		ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS categories (
	id	INTEGER PRIMARY KEY,
	name	TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS user_categories (
	category_id	INTEGER NOT NULL,
	user_id	INTEGER NOT NULL,
	CONSTRAINT user_categories_category_id_fkey FOREIGN KEY (category_id)
		REFERENCES categories (id) 
		ON UPDATE NO ACTION ON DELETE NO ACTION,
	CONSTRAINT user_categories_user_id_fkey FOREIGN KEY (user_id)
		REFERENCES users (id) 
		ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS budget_categories (
	budgets_id	INTEGER NOT NULL,
	category_id	INTEGER NOT NULL,
	percent_amount	REAL NOT NULL DEFAULT 0,
	CONSTRAINT budget_categories_budgets_id_fkey FOREIGN KEY (budgets_id)
		REFERENCES budgets(id) 
		ON UPDATE NO ACTION ON DELETE NO ACTION,
	CONSTRAINT budget_categories_category_id_fkey FOREIGN KEY (category_id)
		REFERENCES categories (id) 
		ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS payers (
	id INTEGER PRIMARY KEY, 
	user_id	INTEGER NOT NULL,
	name	TEXT NOT NULL,
	CONSTRAINT payers_user_id_fkey FOREIGN KEY (user_id)
		REFERENCES users (id) 
		ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS "expenses" (
	"id"	INTEGER,
	"description"	TEXT NOT NULL,
	"category_id"	INTEGER NOT NULL,
	"date"	NUMERIC NOT NULL,
	"amount"	REAL NOT NULL,
	"payer_id"	INTEGER NOT NULL,
	"submit_time"	TEXT NOT NULL,
	"user_id"	INTEGER NOT NULL,
	"budget_id"	INTEGER,
	PRIMARY KEY("id"),
	CONSTRAINT "expenses_payer_id_fkey" FOREIGN KEY("payer_id") REFERENCES "payer"("id") ON UPDATE NO ACTION ON DELETE NO ACTION,
	CONSTRAINT "expenses_user_id_fkey" FOREIGN KEY("user_id") REFERENCES "users"("id") ON UPDATE NO ACTION ON DELETE NO ACTION,
	CONSTRAINT "expenses_budget_id_fkey" FOREIGN KEY("budget_id") REFERENCES "budgets"("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

INSERT INTO categories(name) VALUES ('Groceries');
INSERT INTO categories(name) VALUES ('Housing');
INSERT INTO categories(name) VALUES ('Utilities');
INSERT INTO categories(name) VALUES ('Dining Out');
INSERT INTO categories(name) VALUES ('Shopping');
INSERT INTO categories(name) VALUES ('Travel');
INSERT INTO categories(name) VALUES ('Entertainment');
INSERT INTO categories(name) VALUES ('Other');


