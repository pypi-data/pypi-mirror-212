import logging

from dls_utilpack.callsign import callsign
from dls_utilpack.thing import Thing

# Things created in the context.
from soakdb3_lib.datafaces.datafaces import Datafaces

logger = logging.getLogger(__name__)


thing_type = "soakdb3_lib.datafaces.context"


class Context(Thing):
    """
    Asyncio context for a dataface server object.
    On entering, it creates the object according to the specification (a dict).
    If configured, it starts the server as a coroutine, thread or process.
    On exiting, it commands the server to shut down.

    The enter and exit methods are exposed for use during testing.

    TODO: Add unit test for soakdb3_lib.datafaces.context.
    """

    # ----------------------------------------------------------------------------------------
    def __init__(self, specification, predefined_uuid=None):
        Thing.__init__(self, thing_type, specification, predefined_uuid=predefined_uuid)

        # Reference to object which is a server, such as BaseAiohttp.
        self.server = None

        self.context_specification = self.specification().get("context", {})

    # ----------------------------------------------------------------------------------------
    async def aenter(self):
        """ """

        # Build the object according to the specification.
        self.server = Datafaces().build_object(self.specification())

        if self.context_specification.get("start_as") == "coro":
            await self.server.activate_coro()

        elif self.context_specification.get("start_as") == "thread":
            await self.server.start_thread()

        elif self.context_specification.get("start_as") == "process":
            await self.server.start_process()

    # ----------------------------------------------------------------------------------------
    async def aexit(self):
        """
        Asyncio context exit.

        Stop service if one was started and releases any client resources.
        """
        logger.debug(f"[DISSHU] {thing_type} aexit")

        if self.server is not None:
            if self.context_specification.get("start_as") == "process":
                # The server associated with this context is running?
                if await self.is_process_alive():
                    logger.debug(f"[DISSHU] {thing_type} calling client_shutdown")
                    # Put in request to shutdown the server.
                    await self.server.client_shutdown()

            if self.context_specification.get("start_as") == "coro":
                await self.server.direct_shutdown()

    # ----------------------------------------------------------------------------------------
    async def __aenter__(self):
        """ """

        await self.aenter()

    # ----------------------------------------------------------------------------------------
    async def __aexit__(self, type, value, traceback):
        """ """

        await self.aexit()

    # ----------------------------------------------------------------------------------------
    async def is_process_started(self):
        """"""

        if self.server is None:
            raise RuntimeError(f"{callsign(self)} a process has not been defined")

        try:
            return await self.server.is_process_started()
        except Exception:
            raise RuntimeError(
                f"unable to determing process started for server {callsign(self.server)}"
            )

    # ----------------------------------------------------------------------------------------
    async def is_process_alive(self):
        """"""

        if self.server is None:
            raise RuntimeError(f"{callsign(self)} a process has not been defined")

        try:
            return await self.server.is_process_alive()
        except Exception:
            raise RuntimeError(
                f"unable to determing dead or alive for server {callsign(self.server)}"
            )
