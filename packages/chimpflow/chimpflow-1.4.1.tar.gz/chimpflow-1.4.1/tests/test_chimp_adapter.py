import logging
import multiprocessing
import uuid
import warnings

import pytest
from dls_utilpack.profiler import dls_utilpack_global_profiler
from xchembku_api.models.crystal_well_autolocation_model import (
    CrystalWellAutolocationModel,
)
from xchembku_api.models.crystal_well_model import CrystalWellModel

from chimpflow_api.constants import WELL_CENTROID_ALGORITHMS

# Base class for the tester.
from tests.base import Base

with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    # Chimp adapter object.
    from chimpflow_lib.chimp_adapter import ChimpAdapter


logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------------------
class TestChimpAdapter:
    """
    Test chimp adapter ability to process chimp images.
    """

    def test(self, constants, logging_setup, output_directory):

        ChimpAdapterTester().main(constants, None, output_directory)


# ----------------------------------------------------------------------------------------
class ChimpAdapterTester(Base):
    """ """

    # ----------------------------------------------------------------------------------------
    async def _main_coroutine(self, constants, output_directory):
        """ """

        # Make a specification for the chimp adapter.
        self.__specification = {
            "model_path": constants["model_path"],
            "num_classes": 3,
            "well_centroid_algorithm": WELL_CENTROID_ALGORITHMS.TEXRANK_LIKE,
        }

        # Do the work in a separate process since the torchvision won't release unless its process quits.
        # If it doesn't release, then subsequent pytest cases wait forever.
        # TODO: Figure out how to release resources from torchvision within a process.
        p = multiprocessing.Process(
            target=self.__process1,
        )
        p.start()
        p.join()
        assert p.exitcode == 0

        # ------------------------------------------------------------------
        # Make a specification for the chimp adapter, this time with no centroid algorithm.
        self.__specification = {
            "model_path": constants["model_path"],
            "num_classes": 3,
            # No specified algorithm.
            # "well_centroid_algorithm": WELL_CENTROID_ALGORITHMS.TEXRANK_LIKE,
        }

        p = multiprocessing.Process(
            target=self.__process2,
        )
        p.start()
        p.join()
        assert p.exitcode == 0

    # ----------------------------------------------------------------------------------------
    def __process1(self):
        chimp_adapter = ChimpAdapter(self.__specification)

        self.__run_97wo_01A_1(chimp_adapter)
        self.__run_97wo_01A_2(chimp_adapter)

        # Display the profiler's end results.
        logger.debug(f"profile\n{dls_utilpack_global_profiler()}")

    # ----------------------------------------------------------------------------------------
    def __process2(self):
        chimp_adapter = ChimpAdapter(self.__specification)

        self.__run_97wo_01A_3(chimp_adapter)

        # Display the profiler's end results.
        logger.debug(f"profile\n{dls_utilpack_global_profiler()}")

    # ----------------------------------------------------------------------------------------
    def __run_97wo_01A_1(self, chimp_adapter: ChimpAdapter) -> None:

        # Make a well model to serve as the input to the chimp adapter process method.
        well_model = CrystalWellModel(
            position="01A_1",
            filename="tests/echo_test_imgs/97wo_01A_1.jpg",
            crystal_plate_uuid=str(uuid.uuid4()),
        )

        # Process the well image and get the resulting autolocation information.
        well_model_autolocation: CrystalWellAutolocationModel = chimp_adapter.detect(
            well_model
        )

        assert well_model_autolocation.drop_detected

        assert well_model_autolocation.number_of_crystals == pytest.approx(30, 1)

        assert well_model_autolocation.auto_target_x == pytest.approx(479, 3)
        assert well_model_autolocation.auto_target_y == pytest.approx(475, 3)

        assert well_model_autolocation.well_centroid_x == 630
        assert well_model_autolocation.well_centroid_y == 494

    # ----------------------------------------------------------------------------------------
    def __run_97wo_01A_2(self, chimp_adapter: ChimpAdapter) -> None:

        # Make a well model to serve as the input to the chimp adapter process method.
        well_model = CrystalWellModel(
            position="01A_2",
            filename="tests/echo_test_imgs/97wo_01A_2.jpg",
            crystal_plate_uuid=str(uuid.uuid4()),
        )

        # Process the well image and get the resulting autolocation information.
        well_model_autolocation: CrystalWellAutolocationModel = chimp_adapter.detect(
            well_model
        )

        assert well_model_autolocation.drop_detected

        assert well_model_autolocation.number_of_crystals == pytest.approx(13, 1)

        assert well_model_autolocation.auto_target_x == pytest.approx(475, 3)
        assert well_model_autolocation.auto_target_y == pytest.approx(745, 3)

        assert well_model_autolocation.well_centroid_x == 630
        assert well_model_autolocation.well_centroid_y == 526

    # ----------------------------------------------------------------------------------------
    def __run_97wo_01A_3(self, chimp_adapter: ChimpAdapter) -> None:

        # Make a well model to serve as the input to the chimp adapter process method.
        well_model = CrystalWellModel(
            position="01A_3",
            filename="tests/echo_test_imgs/97wo_01A_3.jpg",
            crystal_plate_uuid=str(uuid.uuid4()),
        )

        # Process the well image and get the resulting autolocation information.
        well_model_autolocation: CrystalWellAutolocationModel = chimp_adapter.detect(
            well_model
        )

        assert well_model_autolocation.drop_detected

        assert well_model_autolocation.number_of_crystals == pytest.approx(2, 1)

        assert well_model_autolocation.auto_target_x == pytest.approx(417, 3)
        assert well_model_autolocation.auto_target_y == pytest.approx(672, 3)

        # Centroid in this test comes from image central pixel.
        assert well_model_autolocation.well_centroid_x == 612
        assert well_model_autolocation.well_centroid_y == 512
