Odoo Python Client
===============================

![PyPI](https://img.shields.io/pypi/v/odoo-client?style=flat-square)  
Odoo API Client in Python

- Free Software: MIT License
- Examples: TBA

### Installation

```sh
pip install odoo_client
```

### Quickstart
```python
from odoo_client import OdooClient

ODOO_URL = "<Your Odoo URL>"
ODOO_DB = "<Your Odoo Database Name>"
ODOO_USER = "<Your Odoo Username>"
ODOO_PW = "<Your Odoo Password>"

CLIENT = OdooClient(ODOO_URL, ODOO_DB, ODOO_USER, ODOO_PW)

PARTNER = CLIENT.object("res.partner")

# Search for Partners that are companies and return the fields: "name", "country_id" and "comment"
records = PARTNER.search_read([["is_company", "=", True]], ["name", "country_id", "comment"])
```
