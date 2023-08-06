from __future__ import annotations

import logging
import os
import re
from contextlib import contextmanager
from io import BytesIO, IOBase
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, Union

from gql.transport.exceptions import TransportQueryError
from PIL import Image, UnidentifiedImageError
from rich.console import Console
from rich.table import Table

from vectice.api.json.iteration import IterationStatus, IterationStepArtifact
from vectice.api.json.step import StepType

if TYPE_CHECKING:
    from vectice.models.iteration import Iteration
    from vectice.models.step import Step


@contextmanager
def hide_logs(package: str):
    old_level = logging.getLogger(package).level
    try:
        logging.getLogger(package).setLevel(logging.ERROR)
        yield
    finally:
        logging.getLogger(package).setLevel(old_level)


def _check_read_only(iteration: Iteration):
    """Check if an iteration is completed or cancelled.

    Refreshing the iteration is necessary because in a Jupyter notebook
    its status could have changed on the backend.

    Parameters:
        iteration: The iteration to check.

    Raises:
        RuntimeError: When the iteration is read-only (completed or cancelled).
    """
    refresh_iteration = iteration._phase.iteration(iteration.index)
    if refresh_iteration._status in {IterationStatus.Completed, IterationStatus.Abandoned}:
        raise RuntimeError(f"The Iteration is {refresh_iteration.status} and is read-only.")


def _get_step_type(
    id: int,
    iteration: Iteration,
    name: str,
    index: int,
    slug: str,
    step_type: StepType,
    description: str | None = None,
    completed: bool | None = None,
    artifacts: list[IterationStepArtifact] | None = None,
) -> Step | Any:
    # TODO: cyclic imports
    from vectice.models.step import Step
    from vectice.models.step_dataset import StepDataset
    from vectice.models.step_image import StepImage
    from vectice.models.step_model import StepModel
    from vectice.models.step_number import StepNumber
    from vectice.models.step_string import StepString

    step = Step(
        id=id,
        iteration=iteration,
        name=name,
        index=index,
        slug=slug,
        description=description,
        artifacts=artifacts,
        step_type=step_type,
    )

    def _get_number(text):
        try:
            number = float(text)
        except ValueError:
            number = int(text)
        return number

    if artifacts is not None and len(artifacts) >= 1:
        artifact = artifacts[len(artifacts) - 1]
        if step_type is StepType.StepNumber:
            number = _get_number(artifact.text) if artifact.text else None
            return StepNumber(step, number)
        if step_type is StepType.StepString:
            return StepString(step, str(artifact.text))
        if step_type is StepType.StepImage:
            image = _get_image_info(iteration, artifact)
            if image is None:
                return step
            return StepImage(step, image=image)
        if step_type is StepType.StepDataset:
            dataset_version = artifact
            return StepDataset(step, dataset_version=dataset_version)
        if step_type is StepType.StepModel:
            model_version = artifact
            return StepModel(step, model_version=model_version)
    return step


def _get_image_info(iteration: Iteration, artifact: IterationStepArtifact):
    ef_id = artifact.entity_file_id
    if ef_id is None:
        return None

    try:
        image = iteration._client.get_entity_file_by_id(ef_id)
        return image.file_name
    except TransportQueryError:
        return None


def _check_image_path(path: str) -> bool:
    try:
        check_path = Path(path).exists()
    except OSError:
        return False
    _, ext = os.path.splitext(path)
    pillow_extensions = {exten for exten in Image.registered_extensions()}
    if not check_path and ext in pillow_extensions:
        raise ValueError("Check the image path.")
    if not check_path and ext not in pillow_extensions:
        return False
    return True


def _validate_image(path: str) -> BytesIO:
    try:
        byte_io = BytesIO()
        image = Image.open(path)
        image.save(byte_io, image.format)
        image.close()
        byte_io.seek(0)
    except UnidentifiedImageError:
        raise ValueError(f"The provided image {path!r} cannot be opened. Check its format and permissions.") from None
    return byte_io


def _get_image_variables(value: str | IOBase | Image.Image) -> tuple[BytesIO | IOBase, str]:
    if isinstance(value, IOBase):
        image = value
        filename = os.path.basename(value.name)  # type: ignore[attr-defined]
        return image, filename
    if isinstance(value, str):
        image = _validate_image(value)
        filename = os.path.basename(value)
        return image, filename
    if isinstance(value, Image.Image):
        image = value.tobytes()
        filename = os.path.basename(value.filename)
        return image, filename

    raise ValueError("Unsupported image provided.")


def _temp_print(string: str | None = None, table: Table | None = None) -> None:
    console = Console(width=120)
    if string:
        print(string)
        print()
    if table:
        console.print(table)
        print()


def _convert_keys_to_camel_case(input_dict: Dict[str, Any]) -> Dict[str, Union[Any, Dict[str, Any]]]:
    camel_case_dict: Dict[str, Union[Any, Dict[str, Any]]] = {}

    for key, value in input_dict.items():
        camel_case_key = re.sub(r"_([a-z])", lambda match: match.group(1).upper(), key)
        if isinstance(value, dict):
            value = _convert_keys_to_camel_case(value)
        camel_case_dict[camel_case_key] = value

    return camel_case_dict
