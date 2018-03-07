from aiohttp_jwt.utils import deepset


def test_deepset():
    obj = dict()
    deepset(obj, 'foo.bar.baz', 'boo')
    assert obj['foo']['bar']['baz'] == 'boo'
