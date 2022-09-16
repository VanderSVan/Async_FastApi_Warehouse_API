from src.api.crud_operations.base_crud_operations import ModelOperation
from src.api.models.warehouse_group import WarehouseGroupModel


class WarehouseGroupOperation(ModelOperation):
    def __init__(self, db):
        self.model = WarehouseGroupModel
        self.model_name = 'warehouse group'
        self.db = db
