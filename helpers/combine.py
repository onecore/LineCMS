keys = {
    "orders" : ['id','fulfilled','customer_name', 'customer_email', 'amount_total', 'created', 'payment_status', 'customer_country', 'customer_postal', 'currency', 'items', 'session_id', 'metadata', 'address', 'phone', 'shipping_cost','history','ordernumber','additional']
}

def zipper(key,combinewith):
    return dict(zip(keys[key],combinewith))
    