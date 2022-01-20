from datetime import date
from dataclasses import dataclass
from typing import NewType, Optional

@dataclass(frozen=True)
class OrderLine:
    order_ref : int
    sku : str
    quantity : int

class Batch:
    def __init__(self, id: int, sku: str, quantity: int, eta: Optional[date]):
       self.id = id
       self.sku = sku
       self.eta = eta
       self._purchased_quantity = quantity
       self._allocations = set()

    def can_allocate(self, line: OrderLine) -> bool:
        return line.sku == self.sku and line.quantity <= self.available_quantity

    def allocate(self, line: OrderLine):
        if self.can_allocate(line):
            self._allocations.add(line)
    
    def deallocate(self, line: OrderLine):
        if line in self._allocations:
             self._allocations.remove(line)

    @property
    def allocated_quantity(self) -> int:
        return sum(line.quantity for line in self._allocations)

    @property
    def available_quantity(self) -> int:
        return self._purchased_quantity - self.allocated_quantity



    