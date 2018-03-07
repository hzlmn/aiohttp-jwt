def deepset(obj, path, value):
    """Setting nested properties on object with dot notatiion"""
    parts = path.split('.')
    length = len(parts)
    lastId = length - 1
    target = obj
    for idx, part in enumerate(parts):
        if idx == lastId:
            target[part] = value
            break
        if not target.get(part):
            target[part] = dict()
        target = target[part]
    return obj
