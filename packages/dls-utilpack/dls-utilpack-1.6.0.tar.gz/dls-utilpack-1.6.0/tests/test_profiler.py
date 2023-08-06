import asyncio
import logging

import pytest

from dls_utilpack.profiler import dls_utilpack_global_profiler

# Base class for the tester.
from tests.base_tester import BaseTester

logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------------------
class TestProfiler(BaseTester):
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

        profiler = dls_utilpack_global_profiler()

        with profiler.context("loop1"):
            await asyncio.sleep(0.1)

        assert profiler.profile("loop1").count == 1
        assert profiler.profile("loop1").seconds == pytest.approx(0.1, abs=1e-2)

        # -----------------------------------------------------
        for i in range(0, 2):
            with profiler.context("loop2"):
                await asyncio.sleep(0.1)

        assert profiler.profile("loop2").count == 2
        assert profiler.profile("loop2").seconds == pytest.approx(0.2, abs=1e-2)

        # -----------------------------------------------------
        # Kind of non-sensical to nest them, but check it anyway.
        with profiler.context("loop3"):
            with profiler.context("loop3"):
                with profiler.context("loop3"):
                    await asyncio.sleep(0.1)

        assert profiler.profile("loop3").count == 3
        assert profiler.profile("loop3").seconds == pytest.approx(0.3, abs=1e-2)

        # -----------------------------------------------------
        s = str(profiler)
        logger.debug(f"profile\n{s}")

        assert "loop1 called 1 times" in s
        assert "loop2 called 2 times" in s
        assert "loop3 called 3 times" in s
