stored_roles = []


def save_roles(roles):
    global stored_roles
    stored_roles = roles


def get_roles():
    return stored_roles