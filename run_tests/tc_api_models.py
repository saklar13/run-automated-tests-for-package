import enum
from typing import Optional

from pydantic.main import BaseModel


class BuildConfOutputModel(BaseModel):
    href: str
    id: str
    name: str
    projectId: str
    projectName: str


class BaseLocatorModel(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None

    def __str__(self):
        return ','.join(map(':'.join, self.dict(exclude_none=True).items()))


class BuildConfLocator(BaseLocatorModel):
    project: Optional[str]
    template: Optional[str]


class BuildStateEnum(enum.Enum):
    QUEUED = 'queued'
    RUNNING = 'running'
    FINISHED = 'finished'


class BuildStatusEnum(enum.Enum):
    SUCCESS = 'SUCCESS'
    FAILURE = 'FAILURE'
    ERROR = 'ERROR'


class QueuedBuildDetailsModel(BaseModel):
    id: int
    state: BuildStateEnum
    status: Optional[BuildStatusEnum]
