from datetime import date

class OrderConsignmentEntity:
    def __init__(
        self,
        external_id: str,
        consignment_unit_id: int,
        consignment_date: date,
        consignment_amount: float
    ):
        self.external_id = external_id
        self.consignment_unit_id = consignment_unit_id
        self.consignment_date = consignment_date
        self.consignment_amount = consignment_amount