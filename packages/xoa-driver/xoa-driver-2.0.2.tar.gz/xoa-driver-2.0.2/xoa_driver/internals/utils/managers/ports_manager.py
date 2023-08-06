from __future__ import annotations
import asyncio
from typing import (
    Awaitable,
    Iterable,
    Type,
    TypeVar,
    Protocol,
    TYPE_CHECKING,
    cast,
)
from collections import OrderedDict
if TYPE_CHECKING:
    from xoa_driver.internals.core import interfaces as itf

from .abc import AbcResourcesManager
from .exceptions import NoSuchPortError


class IPort(Protocol):
    def __init__(self, conn: "itf.IConnection", module_id: int, port_id: int) -> None:
        ...


PT = TypeVar("PT", bound=IPort)


class PortBaseManager(AbcResourcesManager[PT]):
    def obtain(self, key: int) -> PT:
        try:
            return super().obtain(key)
        except KeyError:
            raise NoSuchPortError(key)

    def obtain_multiple(self, *keys: int) -> tuple[PT, ...]:
        try:
            return super().obtain_multiple(*keys)
        except KeyError as err:
            raise NoSuchPortError(err.args[0])


class PortsManager(PortBaseManager[PT]):

    __slots__ = ("_conn", "_ports_type", "_ports_count", "_module_id", )

    def __init__(self, conn: "itf.IConnection", module_id: int, ports_type: Type[PT], ports_count: int) -> None:
        super().__init__()
        self._conn = conn
        self._ports_type = ports_type
        self._ports_count = ports_count
        self._module_id = module_id
        self._items: OrderedDict[int, PT] = OrderedDict(
            (
                port_id,
                self._ports_type(
                    conn=self._conn,
                    module_id=self._module_id,
                    port_id=port_id,
                )
            )
            for port_id in range(self._ports_count)
        )

    async def fill(self) -> None:
        assert not self._lock, "Method <fill> can be called only once."
        coros = cast(Iterable[Awaitable], self._items.values())
        await asyncio.gather(*coros)


class PortResolver(Protocol):
    async def __call__(self, conn: "itf.IConnection", module_id: int, port_id: int) -> Type:
        ...


class PortsCombiManager(PortBaseManager[PT]):

    __slots__ = ("_conn", "_resolver", "_ports_count", "_module_id",)

    def __init__(self, conn: "itf.IConnection", module_id: int, resolver: PortResolver, ports_count: int) -> None:
        super().__init__()
        self._conn = conn
        self._resolver = resolver
        self._ports_count = ports_count
        self._module_id = module_id
        self._items: OrderedDict[int, PT] = OrderedDict()

    async def fill(self) -> None:
        assert not self._lock, "Method <fill> can be called only once."
        coros = iter(
            self._resolver(
                conn=self._conn,
                module_id=self._module_id,
                port_id=port_id,
            )
            for port_id in range(self._ports_count)
        )
        ports = await asyncio.gather(*coros)
        self._items = OrderedDict(
            (port.kind.port_id, port) for port in ports
        )
