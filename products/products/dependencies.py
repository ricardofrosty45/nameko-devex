from nameko import config
from nameko.extensions import DependencyProvider
import redis

from products.exceptions import NotFound

REDIS_URI_KEY = 'REDIS_URI'

class StorageWrapper:
    """
    Product storage

    A very simple example of a custom Nameko dependency. Simplified
    implementation of products database based on Redis key value store.
    Handling the product ID increments or keeping sorted sets of product
    names for ordering the products is out of the scope of this example.

    """

    NotFound = NotFound

    def __init__(self, client):
        self.client = client

    def _format_key(self, product_id):
        return 'products:{}'.format(product_id)

    def _from_hash(self, document):
        try:
            product_id = document[b'id'].decode('utf-8')
        except KeyError:
            product_id = None

        return {
            'id': product_id,
            'title': document.get(b'title', b'').decode('utf-8'),
            'passenger_capacity': int(document.get(b'passenger_capacity', 0)),
            'maximum_speed': int(document.get(b'maximum_speed', 0)),
            'in_stock': int(document.get(b'in_stock', 0))
        }

    def get(self, product_id):
        product = self.client.hgetall(self._format_key(product_id))
        if not product:
            raise NotFound('Product ID {} does not exist'.format(product_id))
        else:
            return self._from_hash(product)

    def list(self):
        keys = self.client.keys(self._format_key('*'))
        for key in keys:
            yield self._from_hash(self.client.hgetall(key))

    def create(self, product):
        self.client.hmset(
            self._format_key(product['id']),
            product)

    def decrement_stock(self, product_id, amount):
        return self.client.hincrby(
            self._format_key(product_id), 'in_stock', -amount)
        
    def delete_product_by_id(self, product_id):
        key = self._format_key(product_id)
        exists = self.client.exists(key)
        if exists:
            self.client.delete(key)
        else:
            raise NotFound('Product ID {} does not exist'.format(product_id))

class Storage(DependencyProvider):

    def setup(self):
        self.client = redis.StrictRedis.from_url(config.get(REDIS_URI_KEY))

    def get_dependency(self, worker_ctx):
        return StorageWrapper(self.client)
