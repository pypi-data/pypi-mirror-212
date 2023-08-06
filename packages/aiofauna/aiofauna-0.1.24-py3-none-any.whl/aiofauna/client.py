import io
import os
from typing import Any as A
from typing import AsyncGenerator as AG
from typing import Dict as D
from typing import Literal
from typing import Optional as O

from aiohttp import ClientSession
from dotenv import load_dotenv

from .datastructures import LazyProxy
from .errors import FaunaException
from .json import to_json
from .objects import Expr

load_dotenv()

Json = D[str, A]
MaybeJson = O[Json]

class FaunaClient(LazyProxy[ClientSession]):
    def __init__(self, secret=None):
        if secret is None:
            secret = os.getenv("FAUNA_SECRET")
        self.secret = secret
    def __load__(self) -> ClientSession:
        return ClientSession()
    async def query(self, expr: Expr) -> MaybeJson:
        async with self.__load__() as session:
            async with session.post(
                "https://db.fauna.com",
                data=to_json(expr),
                headers={
                    "Authorization": f"Bearer {self.secret}",
                    "Content-type": "application/json",
                    "Accept": "application/json",
                },
            ) as response:
                try:
                    data = await response.json()

                    return data["resource"]

                except (
                    FaunaException,
                    ValueError,
                    KeyError,
                    TypeError,
                    Exception,
                ) as exc:
                    return None

    async def stream(self, expr: Expr) -> AG[str, None]:
        """

        `AsyncFaunaClient.stream`


        Summary:


                Streams a FaunaDB document.


        Args:


                expr: A FaunaDB query.


        Returns:


                An Event Stream Generator.
        """

        async with self.__load__() as session:
            async with session.post(
                "https://db.fauna.com",
                data=to_json(expr),
                headers={
                    "Authorization": f"Bearer {self.secret}",
                    "Content-type": "application/json",
                    "Accept": "text/event-stream",
                    "Keep-Alive": "timeout=5, max=900",
                    "Connection": "keep-alive",
                    "Cache-Control": "no-cache",
                    "X-Last-Seen-Txn": "0",
                    "X-Request-By": "aiofauna",
                    "X-Query-By": "aiofauna",
                },
            ) as response:
                with io.StringIO() as buffer:
                    async for chunk in response.content.iter_chunked(1024):
                        buffer.write(chunk.decode())

                        buffer.seek(0)

                        for line in buffer:
                            if line == "\r\n":
                                yield buffer.getvalue()

                                buffer.seek(0)

                                buffer.truncate()

                            else:
                                yield line


Method = Literal['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS', 'TRACE']
        
        
class ApiClient(LazyProxy[ClientSession]):
    def __load__(self) -> ClientSession:
        return ClientSession()
    
    def __init__(self, headers:O[D[str, str]]=None, base_url:O[str]=None, **kwargs):
        self.headers = headers or None
        self.base_url = base_url or ""
        self.kwargs = kwargs
        super().__init__()
        
    async def fetch(self, url:str, method:Method="GET", json:O[D[str,A]]=None, **kwargs) -> D[str,A]:
        """Returns JSON response from url"""
        async with self.__as_proxied__().request(method, self.base_url+url, json=json, **kwargs) as resp:
            try:
                   
                return await resp.json()
            except:
                return {}
            finally:
                await self.__as_proxied__().close()
    async def text(self, url:str, method:Method="GET",**kwargs) -> str:
        """Returns text response from url"""
        async with self.__as_proxied__().request(method, self.base_url+url, **kwargs) as resp:
            try:
                return await resp.text()
            except:
                return ""
        
            finally:
                await self.__as_proxied__().close()   
    async def blob(self, url:str, method:Method="GET", **kwargs) -> bytes:
        """Returns bytes response from url"""
        async with self.__as_proxied__().request(method, self.base_url+url, **kwargs) as resp:
            try:
                return await resp.read()
            except:
                return b""
        
            finally:
                await self.__as_proxied__().close()
            
    async def stream(self, url:str, method:Method="GET", **kwargs) -> AG[bytes, None]:
        """Returns async generator of bytes from url"""
        async with self.__as_proxied__().request(method, self.base_url+url,**kwargs) as resp:
            async for chunk in resp.content.iter_chunked(1024):
                try:
                    yield chunk
                except:
                    pass
                finally:
                    await self.__as_proxied__().close()

        