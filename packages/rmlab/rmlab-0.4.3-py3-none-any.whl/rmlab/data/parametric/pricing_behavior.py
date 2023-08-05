"""A pricing behavior defines the strategy under which flights assign prices to seats."""

import json
from typing import Union
from dataclasses import dataclass
from rmlab._data.conversions import parse_data_from_json
from rmlab._data.enums import FileExtensions, PricingModelKind
from rmlab.data.parametric._pricing_base import PricingModel


@dataclass
class BaseBehaviorModel(PricingModel):
    """Base class for all types of pricing behavior models."""

    pass

@dataclass
class RakeBehaviorModel(BaseBehaviorModel):
    """A kind of pricing behavior model in which a set of seat thresholds are used to allocate seats to fares based on the flight occupation.
    These thresholds can be squeezed with respect to the total flight occupation or shifted up from zero occupation.

    Args:
      zero_shift (float): Per-unit relative displacement of all the thresholds
      squeeze (float): Per-unit relative contraction of the all thresholds

    """

    zero_shift: float
    squeeze: float

@dataclass
class RakeStraightBehaviorModel(RakeBehaviorModel):
    """A kind of pricing behavior model in which a set of seat thresholds are used to allocate seats to fares based on the flight occupation.
    These thresholds are straight, in the sense that the seat limits form a straight line with day before departure.

    Args:
      seats_per_dbd (float): Rate of increase in number of seats per day of all thresholds

    Example
    ```py
    behavior = RakeStraightBehaviorModel(seats_per_dbd=0.15, zero_shift=0.06, squeeze=0.7)
    ```
    """

    seats_per_dbd: float

@dataclass
class RakeEBCBehaviorModel(RakeStraightBehaviorModel):
    """A kind of pricing behavior model in which a set of seat thresholds are derived from an expected booking curve and a confidence level.
    Derives from RakeStraightBehavior to have default rakes when there is no input data from which the EBC is built.
    Args:
        confidence (float): Level from which the thresholds slope is derived.
    Example
    ```py
    behavior = ExpectedBookingCurveThresholds(confidence=0.95, seats_per_dbd=0.15, zero_shift=0.06, squeeze=0.7)
    ```
    """

    confidence: float


def make_pricing_behavior_from_json(
    filename_or_dict: Union[str, dict]
) -> BaseBehaviorModel:
    """Make a pricing behavior instance from a json representation (from file or dict).

    Args:
        filename_or_dict (Union[str, dict]): JSON filename or dictionary in json format

    Examples from dict:
    ```py
    dict_rake_straight_behavior = dic()
    dict_rake_straight_behavior["type"] = "rake_straight"
    dict_rake_straight_behavior["seats_per_dbd"] = 0.15
    dict_rake_straight_behavior["zero_shift"] = 0.06
    dict_rake_straight_behavior["squeeze"] = 0.7
    my_pricing_rake_straight_behavior = make_from_json(dict_rake_straight_behavior)
    ```

    Example from file:
    `my_pricing_rake_straight_behavior.json`
    ```json
    {
      "type" : "rake_straight",
      "seats_per_dbd" : 0.15,
      "zero_shift" : 0.06,
      "squeeze" : 0.7
    }
    ```

    ```py
    my_pricing_rake_straight_behavior = make_pricing_behavior_from_json("my_pricing_behavior.json")
    ```
    """

    model_id, filename, md5hash, content = parse_data_from_json(filename_or_dict)

    if not isinstance(content, dict):
        raise TypeError(f"Expected dict format in {filename_or_dict}")

    content: dict

    if content["type"] == "rake_straight":

        return RakeStraightBehaviorModel(
            id=model_id,
            filename=filename,
            cnt=json.dumps(content),
            hash=md5hash,
            kind=PricingModelKind.BEHAVIOR,
            extension=FileExtensions.JSON,
            seats_per_dbd=float(content["seats_per_dbd"]),
            zero_shift=float(content["zero_shift"]),
            squeeze=float(content["squeeze"]),
        )

    elif content["type"] == "rake_ebc":

        return RakeEBCBehaviorModel(
            id=model_id,
            filename=filename,
            cnt=json.dumps(content),
            hash=md5hash,
            kind=PricingModelKind.BEHAVIOR,
            extension=FileExtensions.JSON,
            seats_per_dbd=float(content["seats_per_dbd"]),
            confidence=float(content["confidence"]),
            zero_shift=float(content["zero_shift"]),
            squeeze=float(content["squeeze"]),
        )

    else:

        raise ValueError(f'Unknown pricing behavior type `{content["type"]}`')
