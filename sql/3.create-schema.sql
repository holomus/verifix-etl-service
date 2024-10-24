CREATE TABLE verifix.smartup_pipe_settings(
  id                    BIGINT         NOT NULL GENERATED ALWAYS AS IDENTITY,
  company_code          VARCHAR(100)   NOT NULL,
  filial_codes          VARCHAR(500)[] NOT NULL,
  host                  VARCHAR(500)   NOT NULL,
  client_id             VARCHAR(500)   NOT NULL,
  client_secret         VARCHAR(500)   NOT NULL,
  last_execution_time   TIMESTAMP,
  CONSTRAINT smartup_pipeline_settings_pk PRIMARY KEY (id)
);

CREATE TABLE verifix.smartup_orders(
  company_code              VARCHAR(100)  NOT NULL,
  deal_id                   BIGINT        NOT NULL,
  filial_code               VARCHAR(500),
  external_id               VARCHAR(500),
  subfilial_code            VARCHAR(500),
  deal_time                 TIMESTAMP     NOT NULL,
  delivery_number           VARCHAR(500),
  delivery_date             DATE          NOT NULL,
  booked_date               DATE          NOT NULL,
  total_amount              NUMERIC(20,6) NOT NULL,
  room_id                   BIGINT        NOT NULL,
  room_code                 VARCHAR(500),
  room_name                 VARCHAR(500)  NOT NULL,
  robot_code                VARCHAR(500),
  lap_code                  VARCHAR(500),
  sales_manager_id          BIGINT        NOT NULL,
  sales_manager_code        VARCHAR(500),
  sales_manager_name        VARCHAR(1000) NOT NULL,
  expeditor_id              BIGINT,
  expeditor_code            VARCHAR(500),
  expeditor_name            VARCHAR(1000),
  person_id                 BIGINT        NOT NULL,
  person_code               VARCHAR(500),
  person_name               VARCHAR(1000) NOT NULL,
  person_local_code         VARCHAR(500),
  person_latitude           NUMERIC(20,15),
  person_longitude          NUMERIC(20,15),
  person_tin                VARCHAR(500),
  currency_code             VARCHAR(500),
  owner_person_code         VARCHAR(500),
  manager_code              VARCHAR(500),
  van_code                  VARCHAR(500),
  contract_code             VARCHAR(500),
  contract_number           VARCHAR(500),
  invoice_number            VARCHAR(500),
  payment_type_code         VARCHAR(500),
  visit_payment_type_code   VARCHAR(500),
  note                      VARCHAR(1000),
  deal_note                 VARCHAR(1000),
  status                    VARCHAR(1000) NOT NULL,
  with_marking              BOOLEAN,
  self_shipment             BOOLEAN,
  total_weight_netto        NUMERIC(20,6),
  total_weight_brutto       NUMERIC(20,6),
  total_litre               NUMERIC(20,6),
  CONSTRAINT smartup_orders_pk PRIMARY KEY (company_code, deal_id)
);

CREATE TABLE verifix.smartup_order_products(
  company_code              VARCHAR(100)  NOT NULL,
  product_unit_id           BIGINT        NOT NULL,
  deal_id                   BIGINT        NOT NULL,
  external_id               VARCHAR(500),
  product_code              VARCHAR(500),
  product_local_code        VARCHAR(500),
  product_name              VARCHAR(500)  NOT NULL,
  serial_number             VARCHAR(500),
  expiry_date               DATE,
  order_quant               NUMERIC(20,6) NOT NULL,
  sold_quant                NUMERIC(20,6) NOT NULL,
  return_quant              NUMERIC(20,6) NOT NULL,
  inventory_kind            VARCHAR(500),
  on_balance                BOOLEAN,
  card_code                 VARCHAR(500),
  warehouse_code            VARCHAR(500),
  product_price             NUMERIC(20,6) NOT NULL,
  margin_amount             NUMERIC(20,6) NOT NULL,
  margin_value              NUMERIC(20,6) NOT NULL,
  margin_kind               VARCHAR(500)  NOT NULL,
  vat_amount                NUMERIC(20,6) NOT NULL,
  vat_percent               NUMERIC(20,6) NOT NULL,
  sold_amount               NUMERIC(20,6) NOT NULL,
  price_type_code           VARCHAR(500),
  CONSTRAINT smartup_order_products_pk PRIMARY KEY (company_code, product_unit_id),
  CONSTRAINT smartup_order_products_f1 FOREIGN KEY (company_code, deal_id) REFERENCES verifix.smartup_orders(company_code, deal_id) ON DELETE CASCADE
);

CREATE INDEX smartup_order_products_i1 ON verifix.smartup_order_products(company_code, deal_id) INCLUDE (product_unit_id);

CREATE TABLE verifix.smartup_order_product_aggregates(
  company_code              VARCHAR(100)  NOT NULL,
  sales_manager_id          BIGINT        NOT NULL,
  filial_code               VARCHAR(500)  NOT NULL,
  room_id                   BIGINT        NOT NULL,
  person_id                 BIGINT        NOT NULL,
  product_code              VARCHAR(500)  NOT NULL,
  delivery_date             DATE          NOT NULL,
  deal_id                   BIGINT        NOT NULL,
  sold_amount               NUMERIC(20,6) NOT NULL,
  sold_quantity             NUMERIC(20,6) NOT NULL,
  sold_weight               NUMERIC(20,6) NOT NULL,
  CONSTRAINT smartup_order_product_aggregates_pk PRIMARY KEY (company_code, sales_manager_id, filial_code, room_id, person_id, product_code, delivery_date)
);

CREATE INDEX smartup_order_product_aggregates_i1 on verifix.smartup_order_product_aggregates(company_code, sales_manager_id, filial_code, delivery_date) INCLUDE (deal_id, sold_amount, sold_quantity, sold_weight);
CREATE INDEX smartup_order_product_aggregates_i2 on verifix.smartup_order_product_aggregates(company_code, sales_manager_id, filial_code, person_id, delivery_date) INCLUDE (deal_id, sold_amount, sold_quantity, sold_weight);
CREATE INDEX smartup_order_product_aggregates_i3 on verifix.smartup_order_product_aggregates(company_code, sales_manager_id, filial_code, product_code, delivery_date) INCLUDE (deal_id, sold_amount, sold_quantity, sold_weight);
CREATE INDEX smartup_order_product_aggregates_i4 on verifix.smartup_order_product_aggregates(company_code, sales_manager_id, filial_code, room_id, delivery_date) INCLUDE (deal_id, sold_amount, sold_quantity, sold_weight);