CREATE TABLE verifix.smartup_pipes(
  id                    BIGINT       NOT NULL GENERATED ALWAYS AS IDENTITY,
  company_code          VARCHAR(100) NOT NULL,
  host                  VARCHAR(500) NOT NULL,
  client_id             VARCHAR(500) NOT NULL,
  client_secret         VARCHAR(500) NOT NULL,
  CONSTRAINT smartup_pipes_pk PRIMARY KEY (id),
  CONSTRAINT smartup_pipes_u1 UNIQUE (company_code, host)
);

CREATE TABLE verifix.smartup_cursors(
  pipe_id                   BIGINT       NOT NULL,
  extraction_key            VARCHAR(100) NOT NULL,
  last_cursor               BIGINT       NOT NULL,
  CONSTRAINT smartup_cursors_pk PRIMARY KEY (pipe_id, extraction_key),
  CONSTRAINT smartup_cursors_f1 FOREIGN KEY (pipe_id) REFERENCES verifix.smartup_pipes(id) ON DELETE CASCADE
);

CREATE TABLE verifix.smartup_legal_persons(
  pipe_id                   BIGINT        NOT NULL,
  person_id                 BIGINT        NOT NULL,
  name                      VARCHAR(1000) NOT NULL,
  short_name                VARCHAR(1000) NOT NULL,
  region_id                 BIGINT,
  CONSTRAINT smartup_legal_persons_pk PRIMARY KEY (pipe_id, person_id),
  CONSTRAINT smartup_legal_persons_f1 FOREIGN KEY (pipe_id) REFERENCES verifix.smartup_pipes(id) ON DELETE CASCADE
);

CREATE INDEX smartup_legal_persons_i1 on verifix.smartup_legal_persons(pipe_id, region_id);

CREATE TABLE verifix.smartup_legal_person_types(
  pipe_id                   BIGINT        NOT NULL,
  person_group_id           BIGINT        NOT NULL,
  person_id                 BIGINT        NOT NULL,
  person_type_id            BIGINT        NOT NULL,
  CONSTRAINT smartup_legal_person_types_pk PRIMARY KEY (pipe_id, person_group_id, person_id),
  CONSTRAINT smartup_legal_person_types_f1 FOREIGN KEY (pipe_id, person_id) REFERENCES verifix.smartup_legal_persons(pipe_id, person_id) ON DELETE CASCADE
);

CREATE INDEX smartup_legal_person_types_i1 on verifix.smartup_legal_person_types(pipe_id, person_type_id, person_group_id);
CREATE INDEX smartup_legal_person_types_i2 on verifix.smartup_legal_person_types(pipe_id, person_type_id);
CREATE INDEX smartup_legal_person_types_i3 on verifix.smartup_legal_person_types(pipe_id, person_group_id);

CREATE TABLE verifix.smartup_products(
  pipe_id                   BIGINT         NOT NULL,
  product_id                BIGINT         NOT NULL,
  name                      VARCHAR(1000)  NOT NULL,
  weight_netto              NUMERIC(10, 4),
  weight_brutto             NUMERIC(10, 4),
  litr                      NUMERIC(10, 4),
  CONSTRAINT smartup_products_pk PRIMARY KEY (pipe_id, product_id),
  CONSTRAINT smartup_products_f1 FOREIGN KEY (pipe_id) REFERENCES verifix.smartup_pipes(id) ON DELETE CASCADE
);

CREATE TABLE verifix.smartup_product_types(
  pipe_id                   BIGINT         NOT NULL,
  product_group_id          BIGINT         NOT NULL,
  product_id                BIGINT         NOT NULL,
  product_type_id           BIGINT         NOT NULL,
  CONSTRAINT smartup_product_types_pk PRIMARY KEY (pipe_id, product_group_id, product_id),
  CONSTRAINT smartup_product_types_f1 FOREIGN KEY (pipe_id, product_id) REFERENCES verifix.smartup_products(pipe_id, product_id) ON DELETE CASCADE
);

CREATE INDEX smartup_product_types_i1 on verifix.smartup_product_types(pipe_id, product_type_id, product_group_id);
CREATE INDEX smartup_product_types_i2 on verifix.smartup_product_types(pipe_id, product_type_id);
CREATE INDEX smartup_product_types_i3 on verifix.smartup_product_types(pipe_id, product_group_id);

CREATE TABLE verifix.smartup_orders(
  pipe_id                   BIGINT        NOT NULL,
  deal_id                   BIGINT        NOT NULL,
  filial_id                 BIGINT        NOT NULL,
  deal_time                 TIMESTAMP     NOT NULL,
  delivery_date             DATE          NOT NULL,
  booked_date               DATE          NOT NULL,
  room_id                   BIGINT        NOT NULL,
  room_name                 VARCHAR(1000) NOT NULL,
  robot_id                  BIGINT        NOT NULL,
  robot_name                VARCHAR(1000) NOT NULL,
  sales_manager_id          BIGINT        NOT NULL,
  sales_manager_name        VARCHAR(1000) NOT NULL,
  expeditor_id              BIGINT,
  expeditor_name            VARCHAR(1000),
  person_id                 BIGINT        NOT NULL,
  person_name               VARCHAR(1000) NOT NULL,
  currency_id               BIGINT        NOT NULL,
  currency_code             VARCHAR(100)  NOT NULL,
  currency_name             VARCHAR(100)  NOT NULL,
  owner_person_id           BIGINT,
  owner_person_name         VARCHAR(1000),
  manager_id                BIGINT,
  manager_name              VARCHAR(1000),
  status                    VARCHAR(100) NOT NULL,
  CONSTRAINT smartup_orders_pk PRIMARY KEY (pipe_id, deal_id),
  CONSTRAINT smartup_orders_f1 FOREIGN KEY (pipe_id) REFERENCES verifix.smartup_pipes(id) ON DELETE CASCADE
);

CREATE TABLE verifix.smartup_order_products(
  pipe_id                   BIGINT        NOT NULL,
  product_unit_id           BIGINT        NOT NULL,
  deal_id                   BIGINT        NOT NULL,
  product_id                BIGINT        NOT NULL,
  product_name              VARCHAR(500)  NOT NULL,
  serial_number             VARCHAR(500),
  order_quant               NUMERIC(20,6) NOT NULL,
  sold_quant                NUMERIC(20,6) NOT NULL,
  return_quant              NUMERIC(20,6) NOT NULL,
  inventory_kind            VARCHAR(10),
  on_balance                BOOLEAN,
  warehouse_id              BIGINT,
  warehouse_name            VARCHAR(500),
  product_price             NUMERIC(20,6) NOT NULL,
  margin_amount             NUMERIC(20,6) NOT NULL,
  margin_amount_base        NUMERIC(20,6) NOT NULL,
  margin_value              NUMERIC(20,6) NOT NULL,
  margin_kind               VARCHAR(500)  NOT NULL,
  vat_amount                NUMERIC(20,6) NOT NULL,
  vat_percent               NUMERIC(20,6) NOT NULL,
  sold_amount               NUMERIC(20,6) NOT NULL,
  sold_amount_base          NUMERIC(20,6) NOT NUll,
  price_type_id             BIGINT        NOT NULL,
  price_type_name           VARCHAR(500)  NOT NULL,
  CONSTRAINT smartup_order_products_pk PRIMARY KEY (pipe_id, product_unit_id),
  CONSTRAINT smartup_order_products_f1 FOREIGN KEY (pipe_id, deal_id) REFERENCES verifix.smartup_orders(pipe_id, deal_id) ON DELETE CASCADE
);

CREATE INDEX smartup_order_products_i1 ON verifix.smartup_order_products(pipe_id, deal_id) INCLUDE (product_unit_id);

CREATE TABLE verifix.smartup_order_product_aggregates(
  pipe_id                   BIGINT        NOT NULL,
  sales_manager_id          BIGINT        NOT NULL,
  filial_id                 BIGINT        NOT NULL,
  room_id                   BIGINT        NOT NULL,
  person_id                 BIGINT        NOT NULL,
  product_id                BIGINT        NOT NULL,
  delivery_date             DATE          NOT NULL,
  deal_count                NUMERIC(20,6) NOT NULL,
  sold_amount               NUMERIC(20,6) NOT NULL,
  sold_quantity             NUMERIC(20,6) NOT NULL,
  sold_weight               NUMERIC(20,6) NOT NULL,
  CONSTRAINT smartup_order_product_aggregates_pk PRIMARY KEY (pipe_id, sales_manager_id, filial_id, room_id, person_id, product_id, delivery_date),
  CONSTRAINT smartup_order_product_aggregates_f1 FOREIGN KEY (pipe_id) REFERENCES verifix.smartup_pipes(id) ON DELETE CASCADE
);

CREATE INDEX smartup_order_product_aggregates_i1 on verifix.smartup_order_product_aggregates(pipe_id, sales_manager_id, filial_id, delivery_date) INCLUDE (deal_count, sold_amount, sold_quantity, sold_weight);
CREATE INDEX smartup_order_product_aggregates_i2 on verifix.smartup_order_product_aggregates(pipe_id, sales_manager_id, filial_id, person_id, delivery_date) INCLUDE (deal_count, sold_amount, sold_quantity, sold_weight);
CREATE INDEX smartup_order_product_aggregates_i3 on verifix.smartup_order_product_aggregates(pipe_id, sales_manager_id, filial_id, product_id, delivery_date) INCLUDE (deal_count, sold_amount, sold_quantity, sold_weight);
CREATE INDEX smartup_order_product_aggregates_i4 on verifix.smartup_order_product_aggregates(pipe_id, sales_manager_id, filial_id, room_id, delivery_date) INCLUDE (deal_count, sold_amount, sold_quantity, sold_weight);