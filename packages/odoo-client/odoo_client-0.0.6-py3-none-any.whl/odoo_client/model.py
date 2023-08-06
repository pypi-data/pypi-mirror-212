from xmlrpc.client import ServerProxy

from odoo_client.decorators import handle_exception


class OdooModel:
    def __init__(self,
                 url: str,
                 user_id: int,
                 database: str,
                 password: str):
        self.url = url
        self.user_id = user_id
        self.database = database
        self.password = password
        self.models = ServerProxy(f"{self.url}/xmlrpc/2/object")

    @handle_exception
    def create_model(self,
                     name: str) -> int:
        payload = {
            "name": name,
            "model": f"x_{'_'.join(name.lower().split(' '))}",
            "state": "manual"
        }
        return self.models.execute_kw(self.database,
                                      self.user_id,
                                      self.password,
                                      "ir.model",
                                      "create",
                                      payload)

    @handle_exception
    def create_model_field(self,
                           model: int,
                           name: str,
                           field_type: str,
                           required: bool) -> int:
        payload = {
            "model_id": model,
            "name": f"x_{name}",
            "ttype": field_type,
            "state": "manual",
            "required": required
        }
        return self.models.execute_kw(self.database,
                                      self.user_id,
                                      self.password,
                                      "ir.model.fields",
                                      "create",
                                      payload)
