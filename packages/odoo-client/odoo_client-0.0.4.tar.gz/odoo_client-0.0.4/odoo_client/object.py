from typing import List, Union
from xmlrpc.client import ServerProxy


class OdooObject:
    def __init__(self,
                 name: str,
                 url: str,
                 user_id: int,
                 database: str,
                 password: str):
        self.name = name
        self.url = url
        self.user_id = user_id
        self.database = database
        self.password = password
        self.models = ServerProxy(f"{self.url}/xmlrpc/2/object")

    def check_access_rights(self) -> bool:
        return self.models.execute_kw(self.database,
                                      self.user_id,
                                      self.password,
                                      self.name,
                                      "check_access_rights",
                                      ["read"],
                                      {"raise_exception": False})

    def count_records(self,
                      query: List[List[Union[str, int, bool]]]) -> int:
        return self.models.execute_kw(self.database,
                                      self.user_id,
                                      self.password,
                                      self.name,
                                      "search_count",
                                      [query])

    def create_record(self,
                      payload: dict) -> int:
        return self.models.execute_kw(self.database,
                                      self.user_id,
                                      self.password,
                                      self.name,
                                      "create",
                                      [payload])

    def delete_records(self,
                       pks: List[int]) -> bool:
        return self.models.execute_kw(self.database,
                                      self.user_id,
                                      self.password,
                                      self.name,
                                      "unlink",
                                      [pks])

    def get_fields(self) -> dict:
        return self.models.execute_kw(self.database,
                                      self.user_id,
                                      self.password,
                                      self.name,
                                      "fields_get",
                                      [],
                                      {"attributes": ["string", "help", "type"]})

    def list_records(self,
                     query: List[List[Union[str, int, bool]]],
                     pagination: Union[dict, None] = None) -> List[int]:
        if pagination:
            return self.models.execute_kw(self.database,
                                          self.user_id,
                                          self.password,
                                          self.name,
                                          "search",
                                          [query],
                                          pagination)
        return self.models.execute_kw(self.database,
                                      self.user_id,
                                      self.password,
                                      self.name,
                                      "search",
                                      [query])

    def read_records(self,
                     pks: List[int],
                     fields: Union[List[str], None] = None) -> List[dict]:
        if fields:
            return self.models.execute_kw(self.database,
                                          self.user_id,
                                          self.password,
                                          self.name,
                                          "read",
                                          [pks],
                                          {"fields": fields})
        return self.models.execute_kw(self.database,
                                      self.user_id,
                                      self.password,
                                      self.name,
                                      "read",
                                      [pks])

    def search_read(self,
                    query: List[List[Union[str, int, bool]]],
                    fields: List[str],
                    limit: int = None) -> List[dict]:
        context = {"fields": fields}
        if limit is not None:
            context.update({"limit": limit})
        return self.models.execute_kw(self.database,
                                      self.user_id,
                                      self.password,
                                      self.name,
                                      "search_read",
                                      [query],
                                      context)

    def update_record(self,
                      pk: int,
                      payload: dict) -> bool:
        return self.models.execute_kw(self.database,
                                      self.user_id,
                                      self.password,
                                      self.name,
                                      "write",
                                      [[pk], payload])
