def page_check(page_number, page_size):
    page = {"number": 1, "size": 50}
    if not (isinstance(page_size, int) or page_size is None) or (
            not (isinstance(page_number, int) or page_number is None)):
        raise ValueError("pagination values is wrong")
    if page_number is not None:
        page["number"] = page_number
    if page_size is not None:
        page["size"] = page_size
    return page

def items_val_check(sort, page_number, page_size):
    if sort is not None:
        sort = sort + ":desc"
    page = page_check(page_number=page_number, page_size=page_size)
    return sort, page