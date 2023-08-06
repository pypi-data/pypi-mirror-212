import time
from abc import ABC, abstractmethod
from typing import Optional

from hostingde.model.filter import FilterCondition, FilterElement
from hostingde.model.job import Job
from hostingde.model.sort import SortConfiguration
from hostingde.paginator import HostingDePaginator


class AsynchronousClient(ABC):
    @abstractmethod
    def jobs_find(
        self,
        limit: Optional[int] = None,
        filter: Optional[FilterElement] = None,
        sort: Optional[SortConfiguration] = None,
        *args: list,
        **kwargs: dict
    ) -> HostingDePaginator[Job]:
        """
        Retrieves a list of Job objects from the generic filtering and sorting API.

        :param limit: The limit of objects to retrieve per call. If not set, defaults to 25.
        :param filter: A filter that is applied to the query
        :param sort: Configuration how results are sorted.
        :return: An iterator that yields ZoneConfig objects.
        """
        pass


class JobWaiter:
    def __init__(self, service: AsynchronousClient, id: str, action_name: Optional[str] = None):
        self.service = service
        self.id = id
        self.action_name = action_name

    def wait(self) -> None:
        f = FilterCondition('jobObjectId').eq(self.id) \
            & FilterCondition('jobStatus').ne('successful') \
            & FilterCondition('jobStatus').ne('failed') \
            & FilterCondition('jobStatus').ne('canceled')

        # Append an additional action name filter, if provided
        if self.action_name:
            f = f & FilterCondition('jobType').eq(self.action_name)

        while True:
            jobs = self.service.jobs_find(
                filter=f
            ).fetchall()

            if len(jobs) == 0:
                break

            time.sleep(1)
