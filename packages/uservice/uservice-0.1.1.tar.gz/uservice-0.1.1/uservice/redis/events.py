from typing import Callable

from uservice.entrypoints import Entrypoint
from uservice.contexts import ServiceContext


class RedisEventHandler(Entrypoint):
    def __init__(
            self,
            *,
            context: ServiceContext,
            call: Callable,
            source: str,
            event: str,
    ):
        super().__init__(context=context, call=call)
        self.source = source
        self.event = event
