class OrderProductEntity:
    def __init__(
        self,
        external_id: str,
        product_unit_id: str,
        product_code: str,
        product_name: str,
        order_quant: float,
        product_price: float,
        margin_amount: float,
        margin_kind: str,
        margin_value: float,
        vat_percent: float,
        vat_amount: float,
        sold_amount: float,
        inventory_kind: str,
        price_type_code: str,
        on_balance: bool,
        card_code: str,
        warehouse_code: str
    ):
        self.external_id = external_id
        self.product_unit_id = product_unit_id
        self.product_code = product_code
        self.product_name = product_name
        self.order_quant = order_quant
        self.product_price = product_price
        self.margin_amount = margin_amount
        self.margin_kind = margin_kind
        self.margin_value = margin_value
        self.vat_percent = vat_percent
        self.vat_amount = vat_amount
        self.sold_amount = sold_amount
        self.inventory_kind = inventory_kind
        self.price_type_code = price_type_code
        self.on_balance = on_balance
        self.card_code = card_code
        self.warehouse_code = warehouse_code