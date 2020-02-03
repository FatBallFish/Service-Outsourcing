conn_pool = {1: "123", 2: "456"}
print(conn_pool)
device_id = conn_pool.get(3)
print(device_id)
conn_pool.pop(1)
print(conn_pool)
conn_pool.setdefault(4, "")
print(conn_pool)
