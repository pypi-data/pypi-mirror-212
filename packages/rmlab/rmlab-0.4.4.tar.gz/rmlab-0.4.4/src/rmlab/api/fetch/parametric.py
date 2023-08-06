"""Interface for fetching data related to parametric models and filters."""

from typing import List
from rmlab.data.items import PModel
from rmlab.data.parametric.filter import PFilter
from rmlab._api.fetch import APIFetchInternal
from rmlab._data.enums import CustomersModelKind, ParametricModelKind, PricingModelKind
from rmlab.data.parametric.customers_request import make_customers_request_model_from_json, BaseRequestModel
from rmlab.data.parametric.customers_choice import make_customers_choice_model_from_json, BaseChoiceModel

from rmlab.data.parametric.pricing_range import make_pricing_range_from_json, RangeModel
from rmlab.data.parametric.pricing_behavior import make_pricing_behavior_from_json, BaseBehaviorModel
from rmlab.data.parametric.pricing_optimizer import make_pricing_optimizer_from_json, OptimizerModel



class APIFetchParametric(APIFetchInternal):
    """Exposes functions for fetching flight data from the server."""

    async def fetch_parametric_filters(self, scen_id: int) -> List[PFilter]:
        """Fetch a list of all parametric filters of scenario from server.

        Args:
            scen_id (int): Scenario ID

        Returns:
            List of parametric filters
        """

        return await self._fetch_bounded_items(scen_id, PFilter)

    async def fetch_parametric_models(self, scen_id: int) -> List[PModel]:
        """Fetch a list of all parametric models of scenario from server.

        Args:
            scen_id (int): Scenario ID

        Returns:
            List of parametric models
        """

        return await self._fetch_bounded_items(scen_id, PModel)
    
    async def fetch_customers_request_model(self, scen_id: int, pmodel_id: str) -> BaseRequestModel:
        """Fetch a customers request model from id in scenario
        
        Args:
            scen_id (int): Scenario ID
            pmodel_id (str): Model ID
        
        Returns:
            The requested customers request model
        """

        json = await self._fetch_pmodel(scen_id,
                                  f"{ParametricModelKind.CUSTOMERS.value}_{CustomersModelKind.REQUEST.value}",
                                  pmodel_id)
        
        model = make_customers_request_model_from_json(json)
        model.id = pmodel_id
        return model

    async def fetch_customers_choice_model(self, scen_id: int, pmodel_id: str) -> BaseChoiceModel:
        """Fetch a customers choice model from id in scenario
        
        Args:
            scen_id (int): Scenario ID
            pmodel_id (str): Model ID
        
        Returns:
            The requested customers choice model
        """

        json = await self._fetch_pmodel(scen_id,
                                  f"{ParametricModelKind.CUSTOMERS.value}_{CustomersModelKind.CHOICE.value}",
                                  pmodel_id)
        model = make_customers_choice_model_from_json(json)
        model.id = pmodel_id
        return model

    async def fetch_pricing_range_model(self, scen_id: int, pmodel_id: str) -> RangeModel:
        """Fetch a pricing range model from id in scenario
        
        Args:
            scen_id (int): Scenario ID
            pmodel_id (str): Model ID
        
        Returns:
            The requested pricing range model
        """

        json = await self._fetch_pmodel(scen_id,
                                  f"{ParametricModelKind.PRICING.value}_{PricingModelKind.RANGE.value}",
                                  pmodel_id)
        model = make_pricing_range_from_json(json)
        model.id = pmodel_id
        return model

    async def fetch_pricing_behavior_model(self, scen_id: int, pmodel_id: str) -> BaseBehaviorModel:
        """Fetch a pricing behavior model from id in scenario
        
        Args:
            scen_id (int): Scenario ID
            pmodel_id (str): Model ID
        
        Returns:
            The requested pricing behavior model
        """

        json = await self._fetch_pmodel(scen_id,
                                  f"{ParametricModelKind.PRICING.value}_{PricingModelKind.BEHAVIOR.value}",
                                  pmodel_id)
        model = make_pricing_behavior_from_json(json)
        model.id = pmodel_id
        return model

    async def fetch_pricing_optimizer_model(self, scen_id: int, pmodel_id: str) -> OptimizerModel:
        """Fetch a pricing optimizer model from id in scenario
        
        Args:
            scen_id (int): Scenario ID
            pmodel_id (str): Model ID
        
        Returns:
            The requested pricing optimizer model
        """

        json = await self._fetch_pmodel(scen_id,
                                  f"{ParametricModelKind.PRICING.value}_{PricingModelKind.OPTIMIZER.value}",
                                  pmodel_id)
        model = make_pricing_optimizer_from_json(json)
        model.id = pmodel_id
        return model