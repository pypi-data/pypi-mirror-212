"""Interface for uploading pricing models data."""

import os
from typing import List, Optional, Union
from rmlab_errors import raise_from_list
from rmlab._api.upload import APIUploadInternal
from rmlab._data.enums import (
    CustomersModelKind,
    ParametricModelKind,
)


class APIUploadCustomersModels(APIUploadInternal):
    """Exposes functions for uploading customers models data to the server."""

    async def upload_customers_request_model(
        self,
        scen_id: int,
        content: Union[str, dict],
    ) -> None:
        """Upload to server a parametric model defined in file, modelling how customers request books.

        Args:
            scen_id (int): Scenario ID
            content (str): Request model as file or json dict (require `id` identifier field if the latter)
        """

        await self._upload_parametric_model(
            scen_id,
            parametric_kind=ParametricModelKind.CUSTOMERS,
            kind=CustomersModelKind.REQUEST,
            content=content,
        )

    async def upload_customers_choice_model(
        self,
        scen_id: int,
        content: Union[str, dict],
    ) -> None:
        """Upload to server a parametric model defined in file, modelling how customers choose between competing book offers.

        Args:
            scen_id (int): Scenario ID
            content (str): Request model as file or json dict (require `id` identifier field if the latter)
        """

        await self._upload_parametric_model(
            scen_id,
            parametric_kind=ParametricModelKind.CUSTOMERS,
            kind=CustomersModelKind.CHOICE,
            content=content,
        )

    async def upload_batch_customers_models(
        self,
        scen_id: int,
        *,
        request_models: Optional[List[Union[str, dict]]] = None,
        choice_models: Optional[List[Union[str, dict]]] = None,
    ):
        if request_models is None:
            request_models = list()
        if choice_models is None:
            request_models = list()

        not_found_errors = \
            [FileNotFoundError(fn) for fn in request_models if isinstance(fn, str) and not os.path.exists(fn)] + \
            [FileNotFoundError(fn) for fn in choice_models if isinstance(fn, str) and not os.path.exists(fn)]
        
        type_errors = \
            [TypeError(cnt) for cnt in request_models if (not isinstance(cnt, dict)) and (not isinstance(cnt, str))] + \
            [TypeError(cnt) for cnt in choice_models if not isinstance(cnt, dict) and (not isinstance(cnt, str))]

        raise_from_list(not_found_errors + type_errors)

        for crm in request_models:

            await self._upload_parametric_model(
                scen_id, ParametricModelKind.CUSTOMERS, CustomersModelKind.REQUEST, crm
            )

        for ccm in choice_models:

            await self._upload_parametric_model(
                scen_id, ParametricModelKind.CUSTOMERS, CustomersModelKind.CHOICE, ccm
            )
