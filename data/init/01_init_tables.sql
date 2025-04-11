-- Create the tables
CREATE TABLE category (
  id integer PRIMARY KEY,
  intitule varchar,
  created_at timestamp
);

CREATE TABLE books (
  id integer PRIMARY KEY,
  category_id integer,
  code varchar,
  intitule varchar,
  isbn_10 varchar,
  isbn_13 varchar,
  created_at timestamp
);

CREATE TABLE customers (
  id integer PRIMARY KEY,
  code varchar,
  first_name varchar,
  last_name varchar,
  created_at timestamp
);

CREATE TABLE factures (
  id integer PRIMARY KEY,
  code varchar,
  date_edit varchar,
  customers_id integer,
  qte_totale integer,
  total_amount float,
  total_paid float,
  created_at timestamp
);

CREATE TABLE ventes (
  id integer PRIMARY KEY,
  code varchar,
  date_edit varchar,
  factures_id integer,
  books_id integer,
  pu float,
  qte integer,
  created_at timestamp
);

-- Add foreign keys
ALTER TABLE books ADD FOREIGN KEY (category_id) REFERENCES category (id);
ALTER TABLE ventes ADD FOREIGN KEY (books_id) REFERENCES books (id);
ALTER TABLE ventes ADD FOREIGN KEY (factures_id) REFERENCES factures (id);
ALTER TABLE factures ADD FOREIGN KEY (customers_id) REFERENCES customers (id);