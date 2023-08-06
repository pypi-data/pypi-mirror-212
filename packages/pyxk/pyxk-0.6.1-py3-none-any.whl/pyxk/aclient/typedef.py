from multidict import CIMultiDict
from asyncio import AbstractEventLoop
from typing import Union, Optional

from yarl import URL
from aiohttp import ClientSession, ClientResponse, ClientTimeout


__all__ = ["Session", "EventLoop", "Response", "CIMDict", "StrOrURL", "Timeout"]

EventLoop = Optional[AbstractEventLoop]
Session = Optional[ClientSession]
Response = Optional[ClientResponse]
CIMDict = Optional[CIMultiDict]
StrOrURL = Optional[Union[str, URL]]
Timeout = Optional[Union[int, float, ClientTimeout]]
