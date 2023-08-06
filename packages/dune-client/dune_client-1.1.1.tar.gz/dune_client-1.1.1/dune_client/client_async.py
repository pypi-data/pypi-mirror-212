""""
Async Dune Client Class responsible for refreshing Dune Queries
Framework built on Dune's API Documentation
https://duneanalytics.notion.site/API-Documentation-1b93d16e0fa941398e15047f643e003a
"""
from __future__ import annotations
import asyncio
from typing import Any, Optional, Union

from aiohttp import (
    ClientSession,
    ClientResponse,
    ContentTypeError,
    TCPConnector,
    ClientTimeout,
)

from dune_client.base_client import BaseDuneClient
from dune_client.models import (
    ExecutionResponse,
    DuneError,
    QueryFailed,
    ExecutionStatusResponse,
    ResultsResponse,
    ExecutionState,
)

from dune_client.query import Query


# pylint: disable=duplicate-code
class AsyncDuneClient(BaseDuneClient):
    """
    An asynchronous interface for Dune API with a few convenience methods
    combining the use of endpoints (e.g. refresh)
    """

    _connection_limit = 3

    def __init__(
        self, api_key: str, connection_limit: int = 3, performance: str = "medium"
    ):
        """
        api_key - Dune API key
        connection_limit - number of parallel requests to execute.
        For non-pro accounts Dune allows only up to 3 requests but that number can be increased.
        """
        super().__init__(api_key=api_key, performance=performance)
        self._connection_limit = connection_limit
        self._session: Optional[ClientSession] = None

    async def _create_session(self) -> ClientSession:
        conn = TCPConnector(limit=self._connection_limit)
        return ClientSession(
            connector=conn,
            base_url=self.BASE_URL,
            timeout=ClientTimeout(total=self.DEFAULT_TIMEOUT),
        )

    async def connect(self) -> None:
        """Opens a client session (can be used instead of async with)"""
        self._session = await self._create_session()

    async def disconnect(self) -> None:
        """Closes client session"""
        if self._session:
            await self._session.close()

    async def __aenter__(self) -> AsyncDuneClient:
        self._session = await self._create_session()
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        await self.disconnect()

    async def _handle_response(
        self,
        response: ClientResponse,
    ) -> Any:
        try:
            # Some responses can be decoded and converted to DuneErrors
            response_json = await response.json()
            self.logger.debug(f"received response {response_json}")
            return response_json
        except ContentTypeError as err:
            # Others can't. Only raise HTTP error for not decodable errors
            response.raise_for_status()
            raise ValueError("Unreachable since previous line raises") from err

    async def _get(self, url: str, params: Optional[Any] = None) -> Any:
        if self._session is None:
            raise ValueError("Client is not connected; call `await cl.connect()`")
        self.logger.debug(f"GET received input url={url}")
        response = await self._session.get(
            url=f"{self.API_PATH}{url}",
            headers=self.default_headers(),
            params=params,
        )
        return await self._handle_response(response)

    async def _post(self, url: str, params: Any) -> Any:
        if self._session is None:
            raise ValueError("Client is not connected; call `await cl.connect()`")
        self.logger.debug(f"POST received input url={url}, params={params}")
        response = await self._session.post(
            url=f"{self.API_PATH}{url}",
            json=params,
            headers=self.default_headers(),
        )
        return await self._handle_response(response)

    async def execute(
        self, query: Query, performance: Optional[str] = None
    ) -> ExecutionResponse:
        """Post's to Dune API for execute `query`"""
        params = query.request_format()
        params["performance"] = performance or self.performance

        self.logger.info(
            f"executing {query.query_id} on {performance or self.performance} cluster"
        )
        response_json = await self._post(
            url=f"/query/{query.query_id}/execute",
            params=params,
        )
        try:
            return ExecutionResponse.from_dict(response_json)
        except KeyError as err:
            raise DuneError(response_json, "ExecutionResponse", err) from err

    async def get_status(self, job_id: str) -> ExecutionStatusResponse:
        """GET status from Dune API for `job_id` (aka `execution_id`)"""
        response_json = await self._get(
            url=f"/execution/{job_id}/status",
        )
        try:
            return ExecutionStatusResponse.from_dict(response_json)
        except KeyError as err:
            raise DuneError(response_json, "ExecutionStatusResponse", err) from err

    async def get_result(self, job_id: str) -> ResultsResponse:
        """GET results from Dune API for `job_id` (aka `execution_id`)"""
        response_json = await self._get(url=f"/execution/{job_id}/results")
        try:
            return ResultsResponse.from_dict(response_json)
        except KeyError as err:
            raise DuneError(response_json, "ResultsResponse", err) from err

    async def get_latest_result(self, query: Union[Query, str, int]) -> ResultsResponse:
        """
        GET the latest results for a query_id without having to execute the query again.

        https://dune.com/docs/api/api-reference/latest_results/
        """
        if isinstance(query, Query):
            params = {
                f"params.{p.key}": p.to_dict()["value"] for p in query.parameters()
            }
            query_id = query.query_id
        else:
            params = None
            query_id = int(query)

        response_json = await self._get(
            url=f"/query/{query_id}/results",
            params=params,
        )
        try:
            return ResultsResponse.from_dict(response_json)
        except KeyError as err:
            raise DuneError(response_json, "ResultsResponse", err) from err

    async def cancel_execution(self, job_id: str) -> bool:
        """POST Execution Cancellation to Dune API for `job_id` (aka `execution_id`)"""
        response_json = await self._post(url=f"/execution/{job_id}/cancel", params=None)
        try:
            # No need to make a dataclass for this since it's just a boolean.
            success: bool = response_json["success"]
            return success
        except KeyError as err:
            raise DuneError(response_json, "CancellationResponse", err) from err

    async def refresh(
        self,
        query: Query,
        ping_frequency: int = 5,
        performance: Optional[str] = None,
    ) -> ResultsResponse:
        """
        Executes a Dune `query`, waits until execution completes,
        fetches and returns the results.
        Sleeps `ping_frequency` seconds between each status request.
        """
        job_id = (await self.execute(query=query, performance=performance)).execution_id
        status = await self.get_status(job_id)
        while status.state not in ExecutionState.terminal_states():
            self.logger.info(
                f"waiting for query execution {job_id} to complete: {status}"
            )
            await asyncio.sleep(ping_frequency)
            status = await self.get_status(job_id)

        full_response = await self.get_result(job_id)
        if status.state == ExecutionState.FAILED:
            self.logger.error(status)
            raise QueryFailed(f"{status}. Perhaps your query took too long to run!")
        return full_response
