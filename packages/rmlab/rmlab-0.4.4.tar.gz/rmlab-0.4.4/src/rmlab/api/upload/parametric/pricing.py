"""Interface for uploading customers models data."""

import os
from typing import List, Optional, Union
from rmlab_errors import raise_from_list
from rmlab._api.upload import APIUploadInternal
from rmlab._data.enums import (
    ParametricModelKind,
    PricingModelKind,
)


class APIUploadPricingModels(APIUploadInternal):
    """Exposes functions for uploading pricing models data to the server."""

    async def upload_pricing_range_model(
        self,
        scen_id: int,
        content: Union[str, dict],
    ) -> None:
        """Upload to server a parametric model defined in file, specifying a pricing range to be applied by flights.

        Args:
            scen_id (int): Scenario ID
            content: Model content as file or json dict (require `id` identifier field if the latter)
        """

        await self._upload_parametric_model(
            scen_id,
            parametric_kind=ParametricModelKind.PRICING,
            kind=PricingModelKind.RANGE,
            content=content,
        )

    async def upload_pricing_behavior_model(
        self,
        scen_id: int,
        content: Union[str, dict],
    ) -> None:
        """Upload to server a parametric model defined in file, specifying the pricing behavior/strategy
        under which flights assign prices to seats.

        Args:
            scen_id (int): Scenario ID
            content: Model content as file or json dict (require `id` identifier field if the latter)
        """

        await self._upload_parametric_model(
            scen_id,
            parametric_kind=ParametricModelKind.PRICING,
            kind=PricingModelKind.BEHAVIOR,
            content=content,
        )

    async def upload_pricing_optimizer_model(
        self,
        scen_id: int,
        content: Union[str, dict],
    ) -> None:
        """Upload to server a parametric model defined in file, specifying the pricing optimization methods
        under which flights operate, to adapt the prices given current and past demand.

        Args:
            scen_id (int): Scenario ID
            content: Model content as file or json dict (require `id` identifier field if the latter)
        """

        await self._upload_parametric_model(
            scen_id,
            parametric_kind=ParametricModelKind.PRICING,
            kind=PricingModelKind.OPTIMIZER,
            content=content,
        )

    async def upload_batch_pricing_models(
        self,
        scen_id: int,
        *,
        range_models: Optional[List[Union[str, dict]]] = None,
        behavior_models: Optional[List[Union[str, dict]]] = None,
        optimizer_models: Optional[List[Union[str, dict]]] = None,
    ):
        if range_models is None:
            range_models = list()
        if behavior_models is None:
            behavior_models = list()
        if optimizer_models is None:
            optimizer_models = list()

        not_existing_filenames = \
            [FileNotFoundError(fn) for fn in range_models if isinstance(fn, str) and not os.path.exists(fn)] + \
            [FileNotFoundError(fn) for fn in behavior_models if isinstance(fn, str) and not os.path.exists(fn)] + \
            [FileNotFoundError(fn) for fn in optimizer_models if isinstance(fn, str) and not os.path.exists(fn)]

        wrong_types = \
            [TypeError("Range model expects dict or file name") for cnt in range_models if (not isinstance(cnt, dict)) and (not isinstance(cnt, str))] + \
            [TypeError("Behavior model expects dict or file name") for cnt in behavior_models if (not isinstance(cnt, dict)) and (not isinstance(cnt, str))] + \
            [TypeError("Optimizer model expects dict or file name") for cnt in optimizer_models if (not isinstance(cnt, dict)) and (not isinstance(cnt, str))]

        raise_from_list(not_existing_filenames + wrong_types)

        for prm in range_models:
            await self._upload_parametric_model(
                scen_id, ParametricModelKind.PRICING, PricingModelKind.RANGE, prm
            )

        for pbm in behavior_models:
            await self._upload_parametric_model(
                scen_id, ParametricModelKind.PRICING, PricingModelKind.BEHAVIOR, pbm
            )

        for pom in optimizer_models:
            await self._upload_parametric_model(
                scen_id, ParametricModelKind.PRICING, PricingModelKind.OPTIMIZER, pom
            )
