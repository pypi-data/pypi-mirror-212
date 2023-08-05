"""
This script provides dataclasses storing arrays representing temporal data of flights.
"""
from dataclasses import dataclass
from datetime import datetime, timezone
from itertools import accumulate
from typing import List, Mapping

from rmlab._data.enums import FlightEvent

_MSecFactor = 1000

@dataclass
class FlightData:
    """Base dataclass for derived classes holding time series data associated to a flight.

    Args:
        id (str): Flight ID to which time series data arrays are associated
        timestamps_array (List[datetime]): Sequence of time stamps with milliseconds granularity
    """

    id: str
    timestamps_array: List[datetime]

    def __post_init__(self):
        if not isinstance(self.timestamps_array, list):
            raise TypeError(f"Expected `list` type in timestamps array. Got `{type(self.timestamps_array)}`")
        if len(self.timestamps_array) > 0:
            if isinstance(self.timestamps_array[0], int):
                # NOTE Assumed input timestamps are in millisec
                self.timestamps_array = [
                    datetime.fromtimestamp(ts / _MSecFactor, tz=timezone.utc) for ts in self.timestamps_array
                ]
            elif not isinstance(self.timestamps_array[0], datetime):
                raise TypeError(f"Expected `datetime` or `int` time for timestamps. Got `{type(self.timestamps_array[0])}`")
            # else timestamps are already a datetime, do nothing
        # else empty array

    def id_serial_timestamps(self):

        if not isinstance(self.timestamps_array, list):
            raise TypeError(f"Expected `list` type in timestamps array. Got `{type(self.timestamps_array)}`")
        if len(self.timestamps_array) > 0:
            if isinstance(self.timestamps_array[0], int):
                return self.id, {"Timestamp": self.timestamps_array}
            elif isinstance(self.timestamps_array[0], datetime):
                return self.id, {"Timestamp": [round(ts.timestamp() * _MSecFactor) for ts in self.timestamps_array]}
            else:
                raise TypeError(f"Expected `datetime` or `int` time for timestamps. Got `{type(self.timestamps_array[0])}`")
        # else empty array

    def is_empty(self):
        return len(self.timestamps_array) == 0


@dataclass
class FlightDataBooks(FlightData):
    """Data class with arrays related to books associated to a flight

    Args:
        fares_array (List[str]): Stores the enabled fares at each time stamp
        pps_array (List[int]): Stores the price per seat associated to each booking in cents
        seats_array (List[int]): Stores the seats booked for each booking
        cumulated_seats_array (List[int]): Stores the cumulated booked seats at each time stamp
        cumulated_revenue_array (List[int]): Stores the cumulated revenue at each time stamp in cents
    """

    fares_array: List[str]
    pps_array: List[int]
    seats_array: List[int]
    cumulated_seats_array: List[int]
    cumulated_revenue_array: List[int]

    def __post_init__(self):
        super().__post_init__()
        if self.cumulated_seats_array is None:
            self.cumulated_seats_array = list(accumulate(self.seats_array))
        if self.cumulated_revenue_array is None:
            self.cumulated_revenue_array = list(accumulate([pps*s for pps, s in zip(self.pps_array, self.seats_array)]))

        assert len(self.fares_array) == len(self.timestamps_array)
        assert len(self.pps_array) == len(self.timestamps_array)
        assert len(self.seats_array) == len(self.timestamps_array)
        assert len(self.cumulated_revenue_array) == len(self.timestamps_array)
        assert len(self.cumulated_seats_array) == len(self.timestamps_array)

    def id_dict(self):
        id, d = self.id_serial_timestamps()
        return id, {**d,
                    "Seats": self.seats_array,
                    "PPS": self.pps_array,
                    "Fares": self.fares_array}


@dataclass
class FlightDataForecastedBooks(FlightData):
    """Data class with arrays related to forecasted books associated to a flight

    Args:
        pps_array (List[float]): Stores the forecasted price per seat at each time stamp
        seats_array (List[float]): Stores the forecasted cumulated booked seats at each time stamp
    """

    pps_array: List[float]
    seats_array: List[float]

    def __post_init__(self):
        super().__post_init__()
        assert len(self.pps_array) == len(self.timestamps_array)
        assert len(self.seats_array) == len(self.timestamps_array)


@dataclass
class FlightDataThresholdSettings(FlightData):
    """Data class with arrays of seat thresholds for each fare associated to a flight

    Args:
        fare_to_threshold_array (Mapping[str], List[int]): Maps each fare identifier
            to an array storing the seat thresholds at each time stamp.
    """

    fare_to_threshold_array: Mapping[str, List[int]]

    def id_dict(self):
        id, d = self.id_serial_timestamps()
        return id, {**d, **self.fare_to_threshold_array}

    def __post_init__(self):
        super().__post_init__()
        assert all([len(threshold) == len(self.timestamps_array)
                    for threshold in self.fare_to_threshold_array.values()])


@dataclass
class FlightDataPricePerSeatSettings(FlightData):
    """Data class with arrays of prices per seat for each fare associated to a flight

    Args:
        fare_to_pps_array (Mapping[str], List[int]): Maps each fare identifier
            to an array storing the prices per seat at each time stamp.
    """

    fare_to_pps_array: Mapping[str, List[int]]

    def id_dict(self):
        id, d = self.id_serial_timestamps()
        return id, {**d, **self.fare_to_pps_array}

    def __post_init__(self):
        super().__post_init__()
        assert all([len(pps) == len(self.timestamps_array)
                    for pps in self.fare_to_pps_array.values()])


@dataclass
class FlightDataEvents(FlightData):
    """Data class holding a sequence of events associated to a flight

    Args:
        events_array (List[FlightEvent]): Stores the events at each time stamp.
    """

    events_array: List[FlightEvent]

    def __post_init__(self):
        super().__post_init__()
        assert len(self.events_array) == len(self.timestamps_array)


@dataclass
class FlightDataQForecast(FlightData):
    """Data class with arrays result of q-forecast.

    Args:
        frat5_array (List[float]): Array of FRAT5 values
        book_qequivalent_array: Array of Q-equivalent books.
    """
    frat5_array: List[float]
    book_qequivalent_array: List[float]

    def __post_init__(self):
        super().__post_init__()
        assert len(self.frat5_array) == len(self.timestamps_array)
        assert len(self.book_qequivalent_array) == len(self.timestamps_array)
