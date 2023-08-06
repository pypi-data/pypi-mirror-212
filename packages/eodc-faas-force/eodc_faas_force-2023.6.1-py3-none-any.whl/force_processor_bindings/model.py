import logging
from enum import Enum
from pathlib import Path

from pydantic import BaseModel, Field, validator

logger = logging.getLogger(__name__)


class ForceResMergeOptions(Enum):
    IMPROPHE = "IMPROPHE"
    REGRESSION = "REGRESSION"
    STARFM = "STARFM"
    NONE = "NONE"

    def __str__(self) -> str:
        """This is so that the template substitution puts in
        the value, without the enum name"""
        return str(self.value)


class ForceParameters(BaseModel):
    """Pydantic model of force supported parameters."""

    input_files: list[str]
    user_workspace: Path
    dem_file: str
    dem_nodata: int = Field(default=-9999)
    do_atmo: bool = Field(default="TRUE")
    do_topo: bool = Field(default="TRUE")
    do_brdf: bool = Field(default="TRUE")
    adjacency_effect: bool = Field(default="TRUE")
    multi_scattering: bool = Field(default="TRUE")
    erase_clouds: bool = Field(default="TRUE")
    max_cloud_cover_frame: int = Field(default=90, ge=0, le=100)
    max_cloud_cover_tile: int = Field(default=90, ge=0, le=100)
    cloud_buffer: float = Field(default=300, ge=0, le=10000)
    cirrus_buffer: float = Field(default=0, ge=0, le=10000)
    shadow_buffer: float = Field(default=90, ge=0, le=10000)
    snow_buffer: float = Field(default=30, ge=0, le=10000)
    cloud_threshold: float = Field(default=0.225, ge=0, le=1)
    shadow_threshold: float = Field(default=0.02, ge=0, le=1)
    res_merge: ForceResMergeOptions = Field(default=ForceResMergeOptions.IMPROPHE)

    @validator(
        "adjacency_effect",
        "do_atmo",
        "do_brdf",
        "do_topo",
        "multi_scattering",
        "erase_clouds",
        allow_reuse=True,
    )
    def bool_to_force_string(cls, v: bool):
        # This is necessary, because the FORCE processor
        # actually needs to take in all-caps strings, not bools.
        return "TRUE" if v is True else "FALSE"
