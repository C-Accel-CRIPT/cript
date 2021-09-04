"""
Experiment Node

"""

from . import CRIPTError
from .base import BaseModel, BaseReference
from .utils.external_database_code import GetMaterial


class ExperimentError(CRIPTError):
    def __init__(self, *msg):
        super().__init__(*msg)


class Experiment(BaseModel):
    _class = "Experiment"
    _error = ExperimentError

    def __init__(
        self,
        name: str,
        c_material=None,
        c_process=None,
        c_data=None,
        funding=None,
        notes: str = None,
        **kwargs
    ):
        """

        :param name: The name of the user.

        :param notes: Any miscellaneous notes related to the user.
        """
        super().__init__(name=name, _class=self._class, notes=notes, **kwargs)

        self._funding = None
        self.funding = funding

        self.c_material = BaseReference("Material", c_material)
        self.c_process = BaseReference("Process", c_process)
        self.c_data = BaseReference("Data", c_data)

    @property
    def funding(self):
        return self._funding

    @funding.setter
    def funding(self, funding):
        self._funding = funding

    def get(self, target):
        return GetMaterial.get(target, self.c_material())
