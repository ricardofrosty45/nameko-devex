import logging

from nameko.events import event_handler
from nameko.rpc import rpc

from products import dependencies, schemas
from products.exceptions import NotFound

logger = logging.getLogger(__name__)

class ProductsService:

    name = 'products'

    storage = dependencies.Storage()

    @rpc
    def get_product(self, product_id):
        """
        List product by id.
        """
        try:
            product = self.storage.get(product_id)
            return schemas.Product().dump(product).data
        except NotFound as e:
            logger.error(f"Product not found: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error while getting product: {str(e)}")
            raise

    @rpc
    def list_products(self):
        """
        List all products.
        """
        try:
            products = self.storage.list()
            return schemas.Product(many=True).dump(products).data
        except Exception as e:
            logger.error(f"Error listing products: {str(e)}")
            raise

    @rpc
    def create_product(self, product):
        """
        Create a new product.
        """
        try:
            product = schemas.Product(strict=True).load(product).data
            self.storage.create(product)
        except Exception as e:
            logger.error(f"Error creating product: {str(e)}")
            raise
    @rpc
    def delete_product(self, product_id):
        """
        Delete a product by id.
        """
        try:
            self.storage.delete_product_by_id(product_id)
        except NotFound as e:
            logger.error(f"Product not found, couldn't delete: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error creating product: {str(e)}")
            raise

    @event_handler('orders', 'order_created')
    def decrement_stock_when_order_created_handler_event(self, payload):
        """
        Handle the creation of an order and decrement stock.
        """
        try:
            for product in payload['order']['order_details']:
                self.storage.decrement_stock(
                    product['product_id'], product['quantity'])
        except Exception as e:
            logger.error(f"Error handling order creation: {str(e)}")
            raise
