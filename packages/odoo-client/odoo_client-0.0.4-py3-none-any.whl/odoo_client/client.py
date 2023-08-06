from typing import Union
from xmlrpc.client import ServerProxy

from odoo_client.model import OdooModel
from odoo_client.object import OdooObject


class OdooClient:
    def __init__(self,
                 url: str,
                 database: str,
                 username: str,
                 password: str):
        self.url = url
        self.database = database
        self.username = username
        self.password = password
        self.user_id: Union[int, None] = None

    def __autheticate(self):
        common = ServerProxy(f"{self.url}/xmlrpc/2/common")
        self.user_id = common.authenticate(self.database, self.username, self.password, {})

    def model(self) -> OdooModel:
        if self.user_id is None:
            self.__autheticate()
        return OdooModel(self.url,
                         self.user_id,
                         self.database,
                         self.password)

    def object(self,
               name: str) -> OdooObject:
        if self.user_id is None:
            self.__autheticate()
        return OdooObject(name,
                          self.url,
                          self.user_id,
                          self.database,
                          self.password)
