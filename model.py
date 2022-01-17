from datetime import date
from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class OrderLine:
    order_ref : int
    sku : str
    quantity : int

class Batch:
    def __init__(self, id: int, sku: str, quantity: int, eta: Optional[date]):
       self.id = id
       self.sku = sku
       self.quantity = quantity
       self.eta = eta

    def allocate(self, line: OrderLine):
        if line.quantity <= self.quantity:
            self.quantity -= line.quantity
            return True
        else:
            return False