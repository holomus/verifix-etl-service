class OrderGiftEntity:
    def __init__(
        self,
        external_id: str,
        product_unit_id: str,
        product_code: str,
        product_name: str,
        order_quant: float,
        warehouse_code: str
    ):
        self.external_id = external_id
        self.product_unit_id = product_unit_id
        self.product_code = product_code
        self.product_name = product_name
        self.order_quant = order_quant
        self.warehouse_code = warehouse_code