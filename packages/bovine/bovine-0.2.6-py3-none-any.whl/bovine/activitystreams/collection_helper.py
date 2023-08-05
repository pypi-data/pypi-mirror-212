class CollectionHelper:
    """Provides the ability to iterate over a Collection or OrderedCollection

    Usage:

    .. code-block:: python

        async for item in CollectionHelper(collection_id, bovine_client):
            do_something(item)

    By setting resolve=True, items are always returned as a dictinary.
    Otherwise, they are returned as a string or dictionary depending on how
    the data is provided by the remote server."""

    def __init__(self, collection_id: str, actor, resolve=False):
        self.actor = actor
        self.collection = collection_id
        self.items = []
        self.resolve = resolve

    def update_items(self):
        if not isinstance(self.collection, dict):
            return False
        if "orderedItems" in self.collection:
            self.items = self.collection["orderedItems"]
            return len(self.items) > 0
        if "items" in self.collection:
            self.items = self.collection["items"]
            return len(self.items) > 0
        return False

    async def resolve_item(self, item):
        if not self.resolve or isinstance(item, dict):
            return item
        return await self.actor.proxy_element(item)

    def __aiter__(self):
        return self

    async def __anext__(self):
        if len(self.items) > 0:
            return await self.resolve_item(self.items.pop(0))
        if isinstance(self.collection, str):
            self.collection = await self.actor.proxy_element(self.collection)
            if self.update_items():
                return await self.resolve_item(self.items.pop(0))
        if "first" in self.collection:
            self.collection = self.collection["first"]
            if self.update_items():
                return await self.resolve_item(self.items.pop(0))
            else:
                return await self.__anext__()
        if "next" in self.collection:
            self.collection = self.collection["next"]
            if self.update_items():
                return await self.resolve_item(self.items.pop(0))
            else:
                return await self.__anext__()

        raise StopAsyncIteration
