from examples import CLIENT

PRODUCT_VARIANT = CLIENT.object("product.product")
PRODUCT_TEMPLATE = CLIENT.object("product.template")

pt_fields = PRODUCT_TEMPLATE.get_fields()

records = PRODUCT_VARIANT.search_read([["active", "=", True]], ["id", "name", "is_product_variant"])

new_record = PRODUCT_VARIANT.create_record({
    "name": "Test Product"
})
