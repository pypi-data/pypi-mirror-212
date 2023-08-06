"""Base tasks to support transferring an arbitrary collection of files to a post-run development location."""
import logging
from abc import ABC
from abc import abstractmethod
from functools import cached_property
from pathlib import Path

from dkist_processing_common.models.tags import Tag
from dkist_processing_common.tasks import WorkflowTaskBase
from dkist_processing_common.tasks.mixin.globus import GlobusMixin
from dkist_processing_common.tasks.mixin.globus import GlobusTransferItem

logger = logging.getLogger(__name__)


class DevDataBase(WorkflowTaskBase):
    """Subclass of WorkflowTaskBase that defines development destination path support."""

    @cached_property
    def destination_bucket(self) -> str:
        """Get the destination bucket."""
        return self.metadata_store_recipe_run_configuration().get("destination_bucket", "dev")

    def format_object_key(self, path: Path) -> str:
        """
        Convert output paths into object store keys.

        Parameters
        ----------
        path: the Path to convert

        Returns
        -------
        formatted path in the object store
        """
        object_key = self.destination_folder / Path(path.name)
        return str(object_key)

    @property
    def destination_folder(self) -> Path:
        """Format the destination folder."""
        dir_name = self.metadata_store_recipe_run_configuration().get("dev_directory_name") or Path(
            self.constants.dataset_id
        )
        return self.destination_root_folder / dir_name

    @property
    def destination_root_folder(self) -> Path:
        """Format the destination root folder."""
        return Path(self.constants.proposal_id)


class TransferDevDataBase(DevDataBase, GlobusMixin, ABC):
    """
    Base class for transferring data to a post-run development location.

    Provides the basic framework of locating and transferring data, but the specific files to be transferred must be
    identified by subclasses.

    Some helper methods that support common conventions are provided:

    o `build_debug_frame_transfer_list` - Transfer all frames tagged with DEBUG

    o `build_intermediate_frame_transfer_list` - Transfer subsets of frames tagged with INTERMEDIATE
    """

    def run(self) -> None:
        """Collect transfer items and send them to Globus for transfer."""
        with self.apm_task_step("Build transfer list"):
            logger.info("Building transfer list")
            transfer_manifest = self.build_transfer_list()

        with self.apm_task_step("Send transfer manifest to globus"):
            logger.info("Sending transfer manifests to globus")
            self.transfer_all_dev_frames(transfer_manifest)

    @abstractmethod
    def build_transfer_list(self) -> list[GlobusTransferItem]:
        """Build a list of all items on scratch to transfer to the development location."""
        pass

    def build_debug_frame_transfer_list(self) -> list[GlobusTransferItem]:
        """Build a transfer list containing all frames tagged with DEBUG."""
        debug_frame_paths: list[Path] = list(self.read(tags=[Tag.debug(), Tag.frame()]))
        transfer_items = []
        for p in debug_frame_paths:
            object_key = self.format_object_key(p)
            destination_path = Path(self.destination_bucket, object_key)
            item = GlobusTransferItem(
                source_path=p,
                destination_path=destination_path,
            )
            transfer_items.append(item)

        return transfer_items

    @property
    def intermediate_task_names(self) -> list[str]:
        """List specifying which TASK types to build when selecting INTERMEDIATE frames."""
        return []

    def build_intermediate_frame_transfer_list(self) -> list[GlobusTransferItem]:
        """
        Build a transfer list containing a subset of frames tagged with INTERMEDIATE.

        More specifically, the intersection of INTERMEDIATE and the tasks defined in `intermediate_task_names`.
        """
        transfer_items = []
        for task in self.intermediate_task_names:
            with self.apm_task_step(f"Build intermediate manifest for {task}"):
                logger.info(f"Building intermediate manifest for {task}")
                transfer_items.extend(self._build_single_task_intermediate_manifest(task=task))

        return transfer_items

    def _build_single_task_intermediate_manifest(self, task: str) -> list[GlobusTransferItem]:
        """Build a transfer list containing all frames tagged with INTERMEDIATE and the given TASK."""
        transfer_items = []
        dark_frames = self.read(tags=[Tag.intermediate(), Tag.task(task)])

        for p in dark_frames:
            tags = self.tags(p)
            output_name = Path(self._construct_intermediate_name_from_tags(tags, task))
            destination_object_key = self.format_object_key(output_name)
            destination_path = Path(self.destination_bucket, destination_object_key)
            item = GlobusTransferItem(
                source_path=p,
                destination_path=destination_path,
            )
            transfer_items.append(item)

        return transfer_items

    def _construct_intermediate_name_from_tags(self, tags: list, task: str) -> str:
        """
        Build a sensible filename from a list of tags on an INTERMEDIATE frame with a specific TASK.

        The name will be `f"INTERMEDIATE_TASK-{task}_[{TAG_STEM}-{TAG_VALUE}, ...].dat"`
        """
        name_parts = []
        for t in tags:
            if t in [Tag.frame(), Tag.intermediate(), Tag.task(task)]:
                continue

            name_parts.append(t.replace("_", "-"))

        name_parts.sort()

        tag_name = "_".join(name_parts)

        return f"INTERMEDIATE_TASK-{task}_" + tag_name + ".dat"

    def transfer_all_dev_frames(self, transfer_items: list[GlobusTransferItem]) -> None:
        """Send a list of transfer items to Globus for transfer."""
        logger.info(
            f"Preparing globus transfer {len(transfer_items)} items: "
            f"recipe_run_id={self.recipe_run_id}. "
            f"transfer_items={transfer_items[:3]}..."
        )

        self.globus_transfer_scratch_to_object_store(
            transfer_items=transfer_items,
            label=f"Transfer science frames for recipe_run_id {self.recipe_run_id}",
        )
