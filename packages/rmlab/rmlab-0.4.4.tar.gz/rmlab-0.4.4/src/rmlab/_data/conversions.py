import hashlib
import json
import os
from typing import Callable, List, Mapping, Tuple, Union

import uuid

from rmlab._data.enums import FlightDataKind, FlightEvent
from rmlab.data.flight import (
    FlightData,
    FlightDataBooks,
    FlightDataEvents,
    FlightDataForecastedBooks,
    FlightDataPricePerSeatSettings,
    FlightDataThresholdSettings,
    FlightDataQForecast
)

UploadableFlightDataType = Union[
    FlightDataBooks, FlightDataThresholdSettings, FlightDataPricePerSeatSettings
]

UploadableDataClassName2DataKind: Mapping[str, FlightDataKind] = {
    FlightDataBooks.__name__: FlightDataKind.ACTUAL_BOOKS,
    FlightDataThresholdSettings.__name__: FlightDataKind.THRESHOLDS_SETTINGS,
    FlightDataPricePerSeatSettings.__name__: FlightDataKind.PRICE_PER_SEAT_SETTINGS,
}

# ---- Server to Client format conversions


def _s2c_conversion_actual_books(flight_id: str, response: dict) -> FlightDataBooks:
    return FlightDataBooks(
        id=flight_id,
        timestamps_array=response["Timestamp"],
        fares_array=response["Fares"],
        pps_array=response["PPS"],
        seats_array=response["Seats"],
        cumulated_seats_array=response["CumSeats"] if "CumSeats" in response else None, # If none, set at post init
        cumulated_revenue_array=response["CumRevenue"] if "CumRevenue" in response else None, # If none, set at post init
    )


def _s2c_conversion_future_books(
    flight_id: str, response: dict
) -> FlightDataForecastedBooks:
    return FlightDataForecastedBooks(
        id=flight_id,
        timestamps_array=response["Timestamp"],
        seats_array=response["AvgSeats"],
        pps_array=response["AvgPPS"],
    )


def _s2c_conversion_thresholds_settings(
    flight_id: str, response: dict
) -> FlightDataThresholdSettings:

    args: Mapping[str, List[int]] = dict()

    for fare_key, fare_threshold in response.items():
        if fare_key != "Timestamp":
            args[fare_key] = fare_threshold

    return FlightDataThresholdSettings(
        id=flight_id,
        timestamps_array=response["Timestamp"],
        fare_to_threshold_array=args,
    )


def _s2c_conversion_price_per_seat_settings(
    flight_id: str, response: dict
) -> FlightDataPricePerSeatSettings:

    args: Mapping[str, List[int]] = dict()

    for fare_key, fare_pps in response.items():
        if fare_key != "Timestamp":
            args[fare_key] = fare_pps

    return FlightDataPricePerSeatSettings(
        id=flight_id, timestamps_array=response["Timestamp"], fare_to_pps_array=args
    )


def _s2c_conversion_events(flight_id: str, response: dict) -> FlightDataEvents:

    return FlightDataEvents(
        id=flight_id,
        timestamps_array=response["Timestamp"],
        events_array=[FlightEvent.str_to_enum_value(e) for e in response["Kind"]],
    )

def _s2c_conversion_forecast(flight_id: str, response: dict) -> FlightDataQForecast:

    return FlightDataQForecast(
        id=flight_id,
        timestamps_array=response["Timestamp"],
        frat5_array=response["FRAT5"],
        book_qequivalent_array=response["BookQE"]
    )


S2C_DataKind2ConvertFunction: Mapping[
    FlightDataKind, Callable[[str, dict], FlightData]
] = {
    FlightDataKind.ACTUAL_BOOKS: _s2c_conversion_actual_books,
    FlightDataKind.EXPECTED_BOOKS: _s2c_conversion_future_books,
    FlightDataKind.DYNAMIC_BOOKS: _s2c_conversion_future_books,
    FlightDataKind.THRESHOLDS_SETTINGS: _s2c_conversion_thresholds_settings,
    FlightDataKind.PRICE_PER_SEAT_SETTINGS: _s2c_conversion_price_per_seat_settings,
    FlightDataKind.EVENTS: _s2c_conversion_events,
    FlightDataKind.FORECAST: _s2c_conversion_forecast,
}


def parse_data_from_json(
    filename_or_var: Union[str, dict, list]
) -> Tuple[str, str, str, Union[dict, list]]:
    """Parse data in json format returning a tuple of (identifier, filename, content)

    Args:
        filename_or_var (Union[str, dict, list]): Filename or instance of `format`

    Raises:
        FileNotFoundError: If filename is not found
        ValueError: If type is not recognized

    Returns:
        Tuple[str, str, Mapping[str, Mapping[str, Any]]]: Tuple with
            model ID, source filename, md5hash of content, and content
    """

    if isinstance(filename_or_var, str):
        if os.path.exists(filename_or_var):
            with open(filename_or_var, "r") as f:
                content = json.loads(f.read())
            model_id = (os.path.basename(filename_or_var).split(".")[-2],)
            filename = filename_or_var
        else:
            raise FileNotFoundError(filename_or_var)
    elif isinstance(filename_or_var, list) or isinstance(filename_or_var, dict):
        content = filename_or_var
        model_id = str(uuid.uuid4())[:16]
        filename = "none"
    else:
        raise ValueError(f"Unhandled type {type(filename_or_var)}")

    return (
        model_id,
        filename,
        hashlib.md5(json.dumps(content).encode()).hexdigest(),
        content,
    )
