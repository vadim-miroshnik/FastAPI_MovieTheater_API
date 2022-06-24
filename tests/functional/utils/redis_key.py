async def make_cache_key(endpoint: str, **kwargs):
    """
    Create structured redis key based on given kwargs
    """
    key_list = [endpoint]
    for arg in sorted(kwargs):
        key_list.append(str(arg))
        key_list.append(str(kwargs[arg]))
    return "::".join(key_list)
