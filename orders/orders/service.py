from nameko.events import EventDispatcher
from nameko.rpc import rpc, RpcProxy
from nameko_sqlalchemy import DatabaseSession
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError
from nameko.exceptions import BadRequest

from orders.exceptions import NotFound, InvalidData, InvalidInput
from orders.models import DeclarativeBase, Order, OrderDetail
from orders.schemas import OrderSchema


class OrdersService:
    name = 'orders'

    db = DatabaseSession(DeclarativeBase)
    event_dispatcher = EventDispatcher()

    @rpc
    def get_order(self, order_id):
        order = self.db.query(Order).get(order_id)

        if not order:
            raise NotFound(f'Order with id {order_id} not found')

        return OrderSchema().dump(order).data
    
    @rpc
    def list_all_orders(self, filter=None, page=1, per_page=40):
        try:
            with self.db.transaction:
                query = self.db.query(Order)

                if filter:
                    query = query.filter_by(**filter)

                offset = (page - 1) * per_page

                
                orders = query.offset(offset).limit(per_page).yield_per(80).all()
        except Exception as e:
            raise BadRequest(f"Failed to retrieve orders: {str(e)}")

        return [OrderSchema().dump(order).data for order in orders]

    @rpc
    def create_order(self, order_details):
        try:
            order = Order(
                order_details=[
                    OrderDetail(
                        product_id=order_detail['product_id'],
                        price=order_detail['price'],
                        quantity=order_detail['quantity']
                    )
                    for order_detail in order_details
                ]
            )
            self.db.add(order)
            self.db.commit()

            order = OrderSchema().dump(order).data

            self.event_dispatcher('order_created', {
                'order': order,
            })

            return order

        except IntegrityError as e:
            raise InvalidData(f'Invalid data: {str(e)}')
        except ValidationError as e:
            raise InvalidData(f'Validation error: {str(e)}')

    @rpc
    def update_order(self, order):
        try:
            order_details = {
                order_detail['id']: order_detail
                for order_detail in order['order_details']
            }

            order = self.db.query(Order).get(order['id'])

            for order_detail in order.order_details:
                order_detail.price = order_details[order_detail.id]['price']
                order_detail.quantity = order_details[order_detail.id]['quantity']

            self.db.commit()
            return OrderSchema().dump(order).data

        except NotFound as e:
            raise e
        except IntegrityError as e:
            self.db.rollback()
            raise InvalidData(f'Invalid data: {str(e)}')
        except ValidationError as e:
            self.db.rollback()
            raise InvalidData(f'Validation error: {str(e)}')

    @rpc
    def delete_order(self, order_id):
        order = self.db.query(Order).get(order_id)

        if not order:
            raise NotFound(f'Order with id {order_id} not found')

        self.db.delete(order)
        self.db.commit()
        
