class OrderActionEntity:
    def __init__(
        self,
        external_id: str,
        product_unit_id: str,
        product_code: str,
        product_name: str,
        order_quant: float,
        bonus_id: int,
        action_name: str
    ):
        self.external_id = external_id
        self.product_unit_id = product_unit_id
        self.product_code = product_code
        self.product_name = product_name
        self.order_quant = order_quant
        self.bonus_id = bonus_id
        self.action_name = action_name