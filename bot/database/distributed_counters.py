import random

from google.cloud import firestore
from google.cloud.firestore_v1 import AsyncDocumentReference


class Shard:
    """
    A shard is a distributed counter. Each shard can support being incremented
    once per second. Multiple shards are needed within a Counter to allow
    more frequent incrementing.
    """

    def __init__(self):
        self._count = 0

    def to_dict(self):
        return {"count": self._count}


class Counter:
    """
    A counter stores a collection of shards which are
    summed to return a total count. This allows for more
    frequent incrementing than a single document.
    """

    def __init__(self, num_shards):
        self._num_shards = num_shards

    async def init_counter(self, doc_ref: AsyncDocumentReference):
        """
        Create a given number of shards as
        subcollection of specified document.
        """
        col_ref = doc_ref.collection("shards")

        # Initialize each shard with count=0
        for num in range(self._num_shards):
            shard = Shard()
            await col_ref.document(str(num)).set(shard.to_dict())

    async def increment_counter(self, doc_ref: AsyncDocumentReference):
        """Increment a randomly picked shard."""
        doc_id = random.randint(0, self._num_shards - 1)

        shard_ref = doc_ref.collection("shards").document(str(doc_id))
        return await shard_ref.update({"count": firestore.Increment(1)})

    async def get_count(self, doc_ref: AsyncDocumentReference):
        """Return a total count across all shards."""
        total = 0
        shards = doc_ref.collection("shards").list_documents()
        async for shard in shards:
            total += (await shard.get()).to_dict().get("count", 0)
        return total
