from src.api.crud_operations.base_crud_operations import ModelOperation
from src.api.models.product import ProductModel


class ProductOperation(ModelOperation):
    def __init__(self, db):
        self.model = ProductModel
        self.model_name = 'product'
        self.db = db
