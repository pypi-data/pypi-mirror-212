import os

from dotenv import load_dotenv

from odoo_client import OdooClient

load_dotenv()

ODOO_URL = os.getenv("ODOO_URL")
ODOO_DB = os.getenv("ODOO_DB")
ODOO_USER = os.getenv("ODOO_USER")
ODOO_PW = os.getenv("ODOO_PW")

CLIENT = OdooClient(ODOO_URL, ODOO_DB, ODOO_USER, ODOO_PW)
