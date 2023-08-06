from rmlab._api.base import APIBaseInternal

class APIPersistence(APIBaseInternal):
    """Interface to interact with data snapshots"""

    async def save_snapshot(self, snapshot_name: str):
        return await self._submit_call("api-snapshot-save", snapshot_name=snapshot_name)

    async def restore_snapshot(self, snapshot_name: str):
        return await self._submit_call("api-snapshot-restore", snapshot_name=snapshot_name)

    async def delete_snapshot(self, snapshot_name: str):
        return await self._submit_call("api-snapshot-delete", snapshot_name=snapshot_name)
    
    async def list_snapshots(self):
        return await self._submit_call("api-snapshot-list")