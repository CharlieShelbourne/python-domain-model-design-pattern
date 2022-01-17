# buisness are implementing new ways of allocating stock and lead times based on what is phisically availiable in the warehouse 
# if a ware house is runs out of a product it is listed outof stock untill the next shipment arrives

# if the system can keep track of shipment and when they arrive we can treat them as real stock (part of the inventory with longer leadtimes)
# sell more stock as items will be out of stock less
# save money as less stock kept in inventory of warehouses

# notes on domain: 
# a product is identified by SKU "skew" (stock-keeping unit)
# an order (placed by customer) order id identified by an order reference: 
#   - comprising of multiple order lines 
#   - each line has a SKU and a quanitity
#   - example: 10 units of RED_CHAIR
# purchasing department orders small batches of stock 
# a batch has a unique ID (reference), a SKU,  a quantity and an ETA
# need to allocate orderline to batches 
# stock from batch sent to customer once arrived 
# when stock allocated by x unts, avaliable quantity is reduced by x units 
# example: bacth of 20 SMALL_TABLE, allocate ordeline for 2 SMALL_TABLE - batch has 18 SMALL_TABLE remaining
# do not allocate to batch if avaliable is less than orderline 
# cannot allocate same line twice - if allocated twice should still see same number in batch 
# batch has an ETA, allocate stock in batches which have stortest ETA or are in warehouse

from model import *
from datetime import date

# unit tests 

# test we allocate stock when given an order (correct stock)
# test stock reduces 
def test_allocating_to_a_batch_reduces_avaliable_quantity():
    batch = Batch(id=0, sku="SMALL-TABLE", quantity=20, eta=date.today())
    orderline = OrderLine(order_ref=0, sku="SMALL-TABLE", quantity=5)
    batch.allocate(orderline)

    assert batch.quantity == 15

# test logit for what we can allocate
def make_batch_and_line(sku, batch_qty, order_qty):
    batch = Batch(id=0, sku=sku, quantity=batch_qty, eta=date.today())
    line = OrderLine(order_ref=100, sku=sku, quantity=order_qty)
    return batch, line

# test we cannot allocate orderline to batch when order is large than stock in batch
def test_small_order_issued_from_large_batch():
    large_batch, small_order = make_batch_and_line("ELEGANT-LAMP", batch_qty=10, order_qty=2)
    assert large_batch.allocate(small_order) is True

def test_large_order_issued_from_small_batch():
    small_batch, large_order = make_batch_and_line("ELEGANT-LAMP", batch_qty=5, order_qty=8)
    assert small_batch.allocate(large_order) is False

def test_order_issued_equal_size_batch():
    batch, order = make_batch_and_line("ELEGANT-LAMP", batch_qty=5, order_qty=5)
    assert batch.allocate(order) is True

# test same orderline cannot be allocate twice 
# test batch with lowest ETA is chosen to allocate 

