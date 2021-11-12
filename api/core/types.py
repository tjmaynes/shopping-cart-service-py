from typing import Protocol, TypeVar


T = TypeVar("T", covariant=True)

class Connection(Protocol[T]):
    def cursor(self):
        pass

    def commit(self):
        pass

    def rollback(self):
        pass

    def close(self):
        pass