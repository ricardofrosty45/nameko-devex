from os import name
from fastapi import APIRouter, status, HTTPException
from fastapi.params import Depends
from typing import List
from gateapi.api import schemas
from gateapi.api.dependencies import get_rpc, config
from .exceptions import OrderNotFound

router = APIRouter(
    prefix = "/orders",
    tags = ['Orders']
)

@router.get("/all", status_code=status.HTTP_200_OK, response_model=List[schemas.Order])
async def get_all_orders(rpc = Depends(get_rpc)):
    try:
        return _list_all_orders(rpc)
    except Exception as error:
        print(str(error)) 
        raise HTTPException(
            status_code=500, 
            detail=str(error)
        )

@router.get("/{order_id}", status_code=status.HTTP_200_OK)
def get_order(order_id: int, rpc = Depends(get_rpc)):
    try:
        return _get_order(order_id, rpc)
    except OrderNotFound as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )

def _list_all_orders(nameko_rpc):
    with nameko_rpc.next() as nameko:
        orders = nameko.orders.list_all_orders()

    with nameko_rpc.next() as nameko:
        product_map = {prod['id']: prod for prod in nameko.products.list_products()}

    image_root = config['PRODUCT_IMAGE_ROOT']

    for order in orders:
        for item in order['order_details']:
            product_id = item['product_id']
            if product_id in product_map:
                item['product'] = product_map[product_id]
                item['image'] = '{}/{}.jpg'.format(image_root, product_id)
            else:
                pass
    return orders

def _get_order(order_id, nameko_rpc):
    with nameko_rpc.next() as nameko:
        order = nameko.orders.get_order(order_id)

    with nameko_rpc.next() as nameko:
        product_map = {prod['id']: prod for prod in nameko.products.list_products()}

    image_root = config['PRODUCT_IMAGE_ROOT']

    for item in order['order_details']:
        product_id = item['product_id']
        item['product'] = product_map[product_id]
        item['image'] = '{}/{}.jpg'.format(image_root, product_id)
    return order

@router.post("", status_code=status.HTTP_200_OK, response_model=schemas.CreateOrderSuccess)
def create_order(request: schemas.CreateOrder, rpc = Depends(get_rpc)):
    id_ =  _create_order(request.dict(), rpc)
    return {
        'id': id_
    }

def _create_order(order_data, nameko_rpc):
    with nameko_rpc.next() as nameko:
        valid_product_ids = {prod['id'] for prod in nameko.products.list_products()}
        for item in order_data['order_details']:
            if item['product_id'] not in valid_product_ids:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail=f"Product with id {item['product_id']} not found"
            )
        result = nameko.orders.create_order(
            order_data['order_details']
        )
        return result['id']