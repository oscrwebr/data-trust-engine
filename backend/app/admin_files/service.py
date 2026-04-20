from app.admin_files import repository


def get_admin_files(search, sensitivity, sort, page, page_size):
    data, total = repository.get_admin_files(
        search=search,
        sensitivity=sensitivity,
        sort=sort,
        page=page,
        page_size=page_size,
    )

    return {
        "data": data,
        "total": total
    }