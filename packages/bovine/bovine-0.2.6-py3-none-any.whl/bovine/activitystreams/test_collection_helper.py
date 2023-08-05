import pytest

from bovine import BovineClient

from .collection_helper import CollectionHelper


@pytest.mark.skip("requires instance requests")
async def test_collections():
    # remote = "https://metalhead.club/users/mariusor/following"
    remote = "FIXME"

    async with BovineClient.from_file("helge.toml") as client:
        collection_helper = CollectionHelper(remote, client, resolve=True)

        async for item in collection_helper:
            print(item)
