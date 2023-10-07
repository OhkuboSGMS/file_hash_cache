from pathlib import Path

from file_hash_cache import AbsTransformIO, FilePath, file_cache_from_file
from base64 import b64encode, b64decode


class Base64Transform(AbsTransformIO[str]):
    def __init__(self, use_cache: bool):
        self.use_cache = use_cache

    def read(self, file_path: FilePath) -> str:
        if not self.use_cache:
            assert False, "Not Call read if self.use_cache == False"
        return Path(file_path).read_text()

    def write(self, data: str, file_path: FilePath) -> FilePath:
        if self.use_cache:
            assert False, "Not Call write if self.use_cache == True"
        path = Path(file_path)
        path.write_text(data)
        return path

    def __call__(self, file_path: FilePath) -> str:
        return b64encode(Path(file_path).read_bytes()).decode()


def test_base64_cache(tmpdir):
    msg = "私はBase64代表です"
    msg_path = Path(tmpdir).joinpath('mochi.txt')
    msg_path.write_text(msg)
    # 1回目
    base_64 = file_cache_from_file(Base64Transform(use_cache=False), tmpdir, msg_path)
    # 2回目
    cached_base_64 = file_cache_from_file(Base64Transform(use_cache=True), tmpdir, msg_path)
    assert base_64 == cached_base_64
    assert msg == b64decode(cached_base_64).decode('utf-8')
