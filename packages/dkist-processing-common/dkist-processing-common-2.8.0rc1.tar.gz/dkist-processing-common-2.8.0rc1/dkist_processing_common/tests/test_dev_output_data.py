import json
from pathlib import Path
from uuid import uuid4

import pytest

from dkist_processing_common.models.graphql import RecipeRunResponse
from dkist_processing_common.models.tags import Tag
from dkist_processing_common.tasks.dev_output_data import DevDataBase
from dkist_processing_common.tasks.dev_output_data import TransferDevDataBase
from dkist_processing_common.tasks.mixin.globus import GlobusTransferItem


class DevDataSubBase(DevDataBase):
    def run(self) -> None:
        ...


@pytest.fixture
def destination_bucket() -> str:
    return "crazy"


@pytest.fixture
def recipe_run_configuration(custom_dir_name, destination_bucket):
    class GQLClientWithConfiguration:
        def __init__(self, *args, **kwargs):
            pass

        def execute_gql_query(self, **kwargs):
            query_base = kwargs["query_base"]
            if query_base == "recipeRuns":
                return [
                    RecipeRunResponse(
                        recipeInstanceId=1,
                        recipeInstance=None,
                        configuration=json.dumps(
                            {
                                "dev_directory_name": custom_dir_name,
                                "destination_bucket": destination_bucket,
                            }
                        ),
                    ),
                ]

        @staticmethod
        def execute_gql_mutation(**kwargs):
            ...

    return GQLClientWithConfiguration


@pytest.fixture
def dev_output_task_base(recipe_run_id, recipe_run_configuration, mocker):
    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient",
        new=recipe_run_configuration,
    )
    proposal_id = "test_proposal_id"
    with DevDataSubBase(
        recipe_run_id=recipe_run_id,
        workflow_name="workflow_name",
        workflow_version="workflow_version",
    ) as task:
        task.constants._update({"PROPOSAL_ID": proposal_id})
        yield task, proposal_id
        task.constants._purge()


@pytest.fixture
def dummy_globus_transfer_item() -> GlobusTransferItem:
    return GlobusTransferItem(source_path="foo", destination_path="bar", recursive=True)


@pytest.fixture
def dev_output_task(dummy_globus_transfer_item):
    class TransferDevData(TransferDevDataBase):
        def build_transfer_list(self) -> list[GlobusTransferItem]:

            transfer_list = [dummy_globus_transfer_item]
            return transfer_list

        @property
        def intermediate_task_names(self) -> list[str]:
            return ["FOO"]

    return TransferDevData


@pytest.fixture
def complete_dev_output_task(recipe_run_id, recipe_run_configuration, dev_output_task, mocker):
    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient",
        new=recipe_run_configuration,
    )
    proposal_id = "test_proposal_id"
    with dev_output_task(
        recipe_run_id=recipe_run_id,
        workflow_name="workflow_name",
        workflow_version="workflow_version",
    ) as task:
        task.constants._update({"PROPOSAL_ID": proposal_id})

        # Write a debug frame
        debug_file_obj = uuid4().hex.encode("utf8")
        task.write(debug_file_obj, relative_path="debug.ext", tags=[Tag.debug(), Tag.frame()])

        # Write an intermediate frame that we want to transfer
        intermediate_keep_file_obj = uuid4().hex.encode("utf8")
        task.write(
            intermediate_keep_file_obj,
            relative_path="intermediate.ext",
            tags=[Tag.intermediate(), Tag.frame(), Tag.task("FOO")],
        )

        # Write an intermediate frame that we don't want to transfer
        intermediate_discard_file_obj = uuid4().hex.encode("utf8")
        task.write(
            intermediate_discard_file_obj,
            tags=[Tag.intermediate(), Tag.frame(), Tag.task("WHO_CARES")],
        )

        yield task, proposal_id, debug_file_obj, intermediate_keep_file_obj
        task.constants._purge()


@pytest.mark.parametrize(
    "custom_dir_name",
    [pytest.param("foo", id="Custom dev dir name"), pytest.param(None, id="Default dev dir name")],
)
def test_format_object_key(dev_output_task_base, custom_dir_name):
    """
    :Given: A base task made from DevDataBase
    :When: Formatting a path into an object key
    :Then: The expected object key is produced and includes a custom dir name if requested
    """
    task, proposal_id = dev_output_task_base
    expected_dir_name = custom_dir_name or task.constants.dataset_id
    filename = "test_filename.ext"
    path = Path(f"a/b/c/d/{filename}")
    assert task.format_object_key(path) == str(Path(proposal_id, expected_dir_name, filename))


@pytest.mark.parametrize("custom_dir_name", [pytest.param(None, id="Default dev dir name")])
def test_build_transfer_list(complete_dev_output_task, dummy_globus_transfer_item):
    """
    Given: A Task based on TransferDevDataBase with a defined build_transfer_list
    When: Building the full transfer list
    Then: The expected transfer list is returned
    """
    task, _, _, _ = complete_dev_output_task
    transfer_list = task.build_transfer_list()

    assert len(transfer_list) == 1
    assert transfer_list[0] == dummy_globus_transfer_item


@pytest.mark.parametrize("custom_dir_name", [pytest.param(None, id="Default dev dir name")])
def test_build_debug_transfer_list(complete_dev_output_task, destination_bucket):
    """
    Given: A Task based on TransferDevDataBase with a tagged DEBUG frame
    When: Building the debug transfer list
    Then: The resulting transfer list has the correct source and destination paths and references the correct frames
    """
    task, proposal_id, debug_file_obj, _ = complete_dev_output_task

    transfer_list = task.build_debug_frame_transfer_list()

    assert len(transfer_list) == 1
    transfer_item = transfer_list[0]
    assert transfer_item.source_path == task.scratch.workflow_base_path / "debug.ext"
    assert transfer_item.destination_path == Path(
        destination_bucket, task.format_object_key(Path("debug.ext"))
    )
    with transfer_item.source_path.open(mode="rb") as f:
        assert debug_file_obj == f.read()


@pytest.mark.parametrize("custom_dir_name", [pytest.param(None, id="Default dev dir name")])
def test_build_intermediate_transfer_list(complete_dev_output_task, destination_bucket):
    """
    Given: A Task based on TransferDevDataBase with tagged INTERMEDIATE frames
    When: Building the intermediate transfer list
    Then: The resulting transfer list has the correct source and destination paths and references the correct frames
    """
    task, proposal_id, _, intermediate_file_obj = complete_dev_output_task

    transfer_list = task.build_intermediate_frame_transfer_list()
    expected_destination_name = task._construct_intermediate_name_from_tags(
        tags=[Tag.intermediate(), Tag.frame(), Tag.task("FOO")], task="FOO"
    )
    expected_destination_path = Path(
        destination_bucket, task.format_object_key(Path(expected_destination_name))
    )

    assert len(transfer_list) == 1
    transfer_item = transfer_list[0]
    assert transfer_item.source_path == task.scratch.workflow_base_path / "intermediate.ext"
    assert transfer_item.destination_path == expected_destination_path
    with transfer_item.source_path.open(mode="rb") as f:
        assert intermediate_file_obj == f.read()
