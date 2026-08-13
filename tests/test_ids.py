from mnemosine.ids import ulid

_ALPHABET = set("0123456789ABCDEFGHJKMNPQRSTVWXYZ")


def test_unique_and_length():
    ids = {ulid() for _ in range(1000)}
    assert len(ids) == 1000
    assert all(len(i) == 26 for i in ids)
    assert all(set(i) <= _ALPHABET for i in ids)


def test_time_sortable():
    import time

    a = ulid()
    time.sleep(0.002)
    b = ulid()
    assert a < b