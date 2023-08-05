from typing import List
from rmlab._api.observability import APIObservabilityInternal


class APIObservability(APIObservabilityInternal):
    """Interface to fetch monitoring data from server."""

    async def fetch_logs(self, context: str, count: int) -> List[str]:
        """Fetch last 'count' monitor logs from the server.

        Args:
            context (str): Logging context, either 'info', 'warning', 'error' or 'critical'
            count (int): Maximum number of log messages. Must be positive.
        
        Raises:
            ValueError: If 'context' or 'count' don't satisfy requirements.

        Returns:
            A list of log messages.
        """

        if context.lower() not in ["info", "warning", "error", "critical"]:
            raise ValueError(f"Expected log context either 'info', 'warning', 'error' or 'critical'")
        
        if not isinstance(count, int) or (isinstance(count, int) and count <= 0):
            raise ValueError(f"Expected 'count' to be a positive integer")

        return await self._fetch_logs(context, count)

    async def fetch_snapshots_list(self):

        return await self._submit_call("api-snapshot-list")