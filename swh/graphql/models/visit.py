from swh.graphql.utils import utils

from .base_model import BaseModel


class VisitModel(BaseModel):
    @property
    def id(self):
        # FIXME, use a better id
        return utils.encode(f"{self.origin}-{str(self.visit)}")
