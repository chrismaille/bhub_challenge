import asyncio
from typing import Callable, Coroutine

from asgiref.sync import SyncToAsync, sync_to_async
from django.db.models import Model


def async_(func: Callable) -> Coroutine | SyncToAsync:
    """Returns a coroutine function."""
    return func if asyncio.iscoroutinefunction(func) else sync_to_async(func)


async def refresh_db(instance: Model):
    """Refresh instance data from database asynchronously."""
    await async_(instance.refresh_from_db)()
