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

def make_cache_key(endpoint: str, **kwargs):
    key_list = [endpoint]
    for arg in sorted(kwargs):
        key_list.append(str(arg))
        key_list.append(str(kwargs[arg]))
    return "::".join(key_list)