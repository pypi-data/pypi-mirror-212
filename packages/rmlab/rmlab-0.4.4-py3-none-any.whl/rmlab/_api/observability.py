from typing import List
from rmlab._api.base import APIBaseInternal

class APIObservabilityInternal(APIBaseInternal):
    """Interface to fetch monitoring data from server."""

    async def _fetch_logs(self, context: str, count: int) -> List[str]:

        return await self._submit_call("api-monitor-activity-user", context=context, count=count)