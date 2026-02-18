wait @app.get("/roles/get")
def get_roles():
    return [
        {"id": 1, "name": "PII"},
        {"id": 2, "name": "Legal"},
        {"id": 3, "name": "Financial"},
    ]