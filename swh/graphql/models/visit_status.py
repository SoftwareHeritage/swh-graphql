from swh.graphql.utils import utils

from .base_model import BaseModel


class VisitStatusModel(BaseModel):
    @property
    def id(self):
        # FIXME, find a proper id
        return utils.encode("temp-id")
