import pytest

from mnemosine import Storage


@pytest.fixture
def db(tmp_path):
    store = Storage(tmp_path / "test.db", blob_root=tmp_path / "blobs")
    store.connect()
    yield store
    store.close()