import pytest


from unittest.mock import Mock, call
from orders.exceptions import NotFound, InvalidData, InvalidInput
from orders.models import Order, OrderDetail
from orders.schemas import OrderSchema, OrderDetailSchema
from orders.service import OrdersService

@pytest.fixture
def order(db_session):
    order = Order()
    db_session.add(order)
    db_session.commit()
    return order

@pytest.fixture
def orders_service():
    return OrdersService()

@pytest.fixture
def order_details(db_session, order):
    db_session.add_all([
        OrderDetail(
            order=order, product_id="the_odyssey", price=99.51, quantity=10
        ),
        OrderDetail(
            order=order, product_id="the_enigma", price=30.99, quantity=10
        )
    ])
    db_session.commit()
    return order_details

@pytest.fixture
def container(config, db_session):
    container = get_container(OrdersService, config)
    container.start()
    yield container
    container.stop()

@pytest.fixture
def test_get_order(orders_rpc, order):
    response = orders_rpc.get_order(1)
    assert response['id'] == order.id
    
def test_can_create_order(orders_service, orders_rpc):
    order_details = [
        {
            'product_id': "the_odyssey",
            'price': 99.99,
            'quantity': 1
        },
        {
            'product_id': "the_enigma",
            'price': 5.99,
            'quantity': 10
        }
    ]
    new_order = orders_rpc.create_order(
        OrderDetailSchema(many=True).dump(order_details).data
    )
    assert new_order['id'] > 0
    assert len(new_order['order_details']) == len(order_details)

@pytest.mark.usefixtures('db_session', 'order_details')

def test_can_update_order(orders_rpc, order):
    order_payload = OrderSchema().dump(order).data
    for order_detail in order_payload['order_details']:
        order_detail['quantity'] += 0

    updated_order = orders_rpc.update_order(order_payload)
    
    for updated_detail in updated_order['order_details']:
        assert updated_detail['quantity'] == 10

@pytest.fixture
def test_can_delete_order(orders_rpc, order, db_session):
    orders_rpc.delete_order(order.id)
    assert not db_session.query(Order).filter_by(id=order.id).count()