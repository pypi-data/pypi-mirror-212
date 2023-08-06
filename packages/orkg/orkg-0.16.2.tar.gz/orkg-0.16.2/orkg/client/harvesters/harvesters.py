from typing import Union

from orkg.common import OID
from orkg.out import OrkgResponse
from orkg.utils import NamespacedClient
from orkg.client.harvesters import doi as doi_harvester


class HarvestersClient(NamespacedClient):

    def doi_harvest(self, doi: str, orkg_rf: Union[str, OID]) -> OrkgResponse:
        """
        Harvests DOI data for a paper and add it to the ORKG.
        It works under the assumption that the paper contains some JSON-LD representation of its content
        :param doi: The DOI of the paper to harvest
        :param orkg_rf: The resource ID of the ORKG research field to add the harvested data to, or the string representation to be looked up (can raise errors)
        """
        return doi_harvester.harvest(self.client, doi, orkg_rf)
