from abc import ABC, abstractmethod
from hashlib import md5, sha1, sha224, sha256, sha384, sha512
from pathlib import Path
from typing import Union, Literal, TypeVar, Generic

T = TypeVar('T')

FilePath = [Union[str, Path]]

_engines = {k: f for f, k in
            zip([md5, sha1, sha224, sha256, sha384, sha512], ["md5", "sha1", "sha224", "sha256", "sha384", "sha512"])}

EngineName = Literal["md5", "sha1", "sha224", "sha256", "sha384", "sha512"]


class AbsTransformIO(ABC, Generic[T]):
    @abstractmethod
    def read(self, file_path: FilePath) -> T:
        pass

    @abstractmethod
    def write(self, data: T, file_path: FilePath) -> FilePath:
        pass

    @abstractmethod
    def __call__(self, file_path: FilePath) -> T:
        pass


def file_cache_from_file(transform: AbsTransformIO, root_path: FilePath, file_path: FilePath,
                         engine: EngineName = "md5") -> T:
    """
    汎用的にファイルのキャッシュを利用できる関数を作成する
    :return:
    """
    hash_f = _engines[engine]
    hashed_name = hash_f(Path(file_path).read_bytes()).hexdigest()
    cached_path = Path(root_path).joinpath(hashed_name)
    # 一度処理が行われて，ファイルとして書き込まれていれば，キャッシュを利用
    if cached_path.exists():
        return transform.read(cached_path)
    # キャッシュファイルが見つからないため，処理を実行し，キャッシュパスにファイルを書き出す
    result = transform(file_path)
    transform.write(result, cached_path)
    return result
