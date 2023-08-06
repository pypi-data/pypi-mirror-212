from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, Iterable, List, TypeVar, cast

from aiohttp.web import FileField
from multidict import CIMultiDictProxy, MultiDict
from pydantic import BaseModel  # pylint: disable=no-name-in-module

T = TypeVar("T")


class LazyProxy(Generic[T], ABC):
    """
    A LazyLoading proxy object that defers the loading of an object until it is accessed.
    It generates types dynamically, so it can be used as a base class for other classes.
    These classes will benefit from the lazy loading behavior which improves performance.
    Also, it can be used as a decorator for functions, which will be called when the function is called.
    Subclasses must implement the __load__ method to provide the logic for loading the proxied object.
    Usage:
    1. Subclass LazyProxy and implement the __load__ method.
    2. Accessing attributes, calling methods, or using other operations on the LazyProxy instance will trigger
         the loading of the proxied object.
    """

    def __init__(self) -> None:
        self.__proxied: T | None = None

    def __getattr__(self, attr: str) -> object:
        return getattr(self.__get_proxied__(), attr)

    def __repr__(self) -> str:
        return repr(self.__get_proxied__())

    def __dir__(self) -> Iterable[str]:
        return self.__get_proxied__().__dir__()

    def __get_proxied__(self) -> T:
        proxied = self.__proxied
        if proxied is not None:
            return proxied

        self.__proxied = proxied = self.__load__()
        return proxied

    def __set_proxied__(self, value: T) -> None:
        self.__proxied = value

    def __as_proxied__(self) -> T:
        """Helper method that returns the current proxy, typed as the loaded object"""
        return cast(T, self)

    @abstractmethod
    def __load__(self) -> T:
        ...

    


class UploadFile(LazyProxy[BaseModel]):
    """
    File Upload Model
    """
    filename: str
    content_type: str
    data: bytes
    size: int
    headers: CIMultiDictProxy[str]
    
    def __init__(self, file: FileField) -> None:
        self.file = file
        self.filename = file.filename
        self.content_type = file.content_type
        self.data = file.file.read()
        self.size = file.file.seek(0, 2)
        self.headers = file.headers
        super().__init__()
        
        
    def __load__(self) -> BaseModel:
        return BaseModel.parse_obj(self.file)