import logging

from dls_utilpack.server_context_base import ServerContextBase

# Base class for the tester.
from tests.base_tester import BaseTester

logger = logging.getLogger(__name__)


class Server:
    # Minimal methods required for a "server" to provide.
    async def is_process_alive(self):
        return True

    async def is_process_started(self):
        return True


class Context(ServerContextBase):
    # For testing.
    def __init__(self, thing_type, specification=None, predefined_uuid=None):
        ServerContextBase.__init__(
            self,
            thing_type,
            specification=specification,
            predefined_uuid=predefined_uuid,
        )

        self.was_entered = 0
        self.was_exited = 0

    # Minimal methods required for a "context" to provide.
    async def aenter(self):
        """ """
        self.was_entered += 1

    async def aexit(self, type, value, traceback):
        """ """
        self.was_exited += 1


# ----------------------------------------------------------------------------------------
class TestServerContext(BaseTester):
    def test(self, constants, logging_setup, output_directory):
        """ """

        self.main(constants, output_directory)

    # ----------------------------------------------------------------------------------------
    async def _main_coroutine(
        self,
        constants,
        output_directory,
    ):
        """ """

        # Make the context.
        context = Context("some::thing")

        # Assign the server.
        context.server = Server()

        # Run the context.
        async with context:
            assert await context.is_process_started()
            assert await context.is_process_alive()

        assert context.was_entered == 1
        assert context.was_exited == 1
