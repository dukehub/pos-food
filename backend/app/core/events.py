from typing import Any, Callable, Dict, List, Type
from dataclasses import dataclass
import asyncio
import logging

logger = logging.getLogger(__name__)

@dataclass
class Event:
    name: str
    payload: Dict[str, Any]

class EventBus:
    def __init__(self):
        self._subscribers: Dict[str, List[Callable[[Event], Any]]] = {}

    def subscribe(self, event_name: str, handler: Callable[[Event], Any]):
        if event_name not in self._subscribers:
            self._subscribers[event_name] = []
        self._subscribers[event_name].append(handler)
        logger.debug(f"Subscribed to {event_name}")

    async def publish(self, event: Event):
        if event.name in self._subscribers:
            tasks = []
            for handler in self._subscribers[event.name]:
                if asyncio.iscoroutinefunction(handler):
                    tasks.append(handler(event))
                else:
                    handler(event)
            
            if tasks:
                await asyncio.gather(*tasks)

event_bus = EventBus()
