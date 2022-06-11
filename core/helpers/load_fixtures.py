import json
from pathlib import Path

import aiofiles

from core import settings


async def load_fixture(app: str, filename: str) -> dict[any, any]:
    """Load fixtures from Django App fixtures folder.

    Example:
    * Add the file `my_response.json` in customers/tests/fixtures
    * In tests load the file using::

        >>> import pytest
        >>> from core.helpers.load_fixtures import load_fixture
        >>>
        >>> @pytest.mark.asyncio
        >>> async def test_load_fixture():
        >>>     data = await load_fixture("customers", "my_response.json")
        >>>     assert data is not None

    For syncronous tests please use async_to_sync decorator.

    param app: Django App folder
    param filename: JSON Filename
    return: Dict
    """
    file_path = Path(settings.BASE_DIR).joinpath(app, "tests", "fixtures", filename)
    async with aiofiles.open(str(file_path)) as file:
        contents = await file.read()
    fixture = json.loads(contents)
    return fixture
