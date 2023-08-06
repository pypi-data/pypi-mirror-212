"""Interface to trigger optimization passes."""

from datetime import datetime
from typing import Optional, List
from rmlab._api.base import APIBaseInternal
from rmlab._data.types import DateTimeMinFormat, DateFormat


class APIOptimization(APIBaseInternal):
    """Exposes functions to run and schedule optimization runs on a set of flights
    and to fetch flights related to optimization targets."""

    async def trigger_optimization_pass(
        self,
        scen_id: int,
        airline_id: str,
        *,
        citysector_id: Optional[str] = None,
        sector_id: Optional[str] = None,
    ):
        """Triggers an optimization pass on all flights of an airline belonging to a citysector or sector.

        Args:
            scen_id (int): Scenario ID
            airline_id (str): Airline ID
            citysector_id (Optional[str], optional): Citysector ID. Defaults to None.
            sector_id (Optional[str], optional): Sector ID. Defaults to None.

        Raises:
            ValueError: If none of `citysector_id`, `sector_id` is defined
        """

        if citysector_id is None and sector_id is None:
            raise ValueError(
                f"At least one of `citysector_id`, `sector_id` must be defined"
            )

        await self._submit_call(
            "api-operation-optimization-trigger",
            scen_id=scen_id,
            airline_id=airline_id,
            citysector_id=citysector_id,
            sector_id=sector_id,
        )

    async def schedule_optimization_pass(
        self,
        scen_id: int,
        airline_id: str,
        date_time: datetime,
        *,
        citysector_id: Optional[str] = None,
        sector_id: Optional[str] = None,
    ):
        """Schedules an optimization pass on all flights of an airline belonging to a citysector or sector to be run at specific date and time.

        Args:
            scen_id (int): Scenario ID
            airline_id (str): Airline ID
            date_time (datetime): Date and time at which the optimization pass is triggered.
            citysector_id (Optional[str], optional): Citysector ID. Defaults to None.
            sector_id (Optional[str], optional): Sector ID. Defaults to None.

        Raises:
            ValueError: If none of `citysector_id`, `sector_id` is defined
        """

        if citysector_id is None and sector_id is None:
            raise ValueError(
                f"At least one of `citysector_id`, `sector_id` must be defined"
            )

        await self._submit_call(
            "api-operation-optimization-schedule",
            scen_id=scen_id,
            date_time=datetime.strftime(date_time, DateTimeMinFormat),
            airline_id=airline_id,
            citysector_id=citysector_id,
            sector_id=sector_id,
        )

    async def fetch_optimization_input_flights(
            self,
            scen_id: int,
            flight_id: str,
            citysector_id: str) -> List[str]:
        """Returns all flights whose data is used as input for optimizing the input flight.

        Args:
            scen_id (int): Scenario ID.
            flight_id (str): Flight ID.
            citysector_id (str): Citysector ID of flight.
        """

        return await self._submit_call(
            "api-operation-optimization-input-ids",
            scen_id=scen_id,
            flight_id=flight_id,
            citysector_id=citysector_id)

    async def fetch_optimization_scheduled_flights(
            self,
            scen_id: int,
            airline_id: str,
            sector_id: str,
            date_start: datetime,
            date_end: datetime) -> List[str]:
        """Returns all flights of an airline in a sector scheduled for optimization passes in a date interval

        Args:
            scen_id (int): Scenario ID.
            airline_id (str): Airline ID.
            sector_id (str): Sector ID of flight.
            date_start (datetime): Start of date interval.
            date_end (datetime): End of date interval.
        """

        return await self._submit_call(
            "api-operation-optimization-scheduled-ids",
            scen_id=scen_id,
            airline_id=airline_id,
            sector_id=sector_id,
            ds_start=datetime.strftime(date_start, DateFormat),
            ds_end=datetime.strftime(date_end, DateFormat))

    async def set_current_date(
            self,
            scen_id: int,
            date_current: datetime):
        """Set current date.

        Args:
            scen_id (int): Scenario ID.
            date_current (datetime): Current date to set.
        """

        if not isinstance(date_current, datetime):
            raise TypeError(f"Expected `datetime` type, got `{type(date_current)}`")

        return await self._submit_call(
            "api-operation-set-date",
            scen_id=scen_id,
            ds_current=datetime.strftime(date_current, DateFormat))
