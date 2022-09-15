from typing import Union
from logging import getLogger

from beartype import beartype

from cript.nodes.primary.base_primary import BasePrimary
from cript.nodes.primary.group import Group
from cript.nodes.primary.project import Project
from cript.nodes.secondary.citation import Citation
from cript.utils import auto_assign_group


logger = getLogger(__name__)


class Collection(BasePrimary):
    """
    Object representing a logical grouping of `Experiment` and
    `Inventory` objects.
    """

    node_name = "Collection"
    slug = "collection"

    @beartype
    def __init__(
        self,
        project: Union[Project, str],
        name: str,
        experiments=None,
        inventories=None,
        notes: Union[str, None] = None,
        citations: list[Union[Citation, dict]] = None,
        public: bool = False,
        group: Union[Group, str] = None,
    ):
        super().__init__(public=public)
        self.project = project
        self.name = name
        self.experiments = experiments if experiments else []
        self.inventories = inventories if inventories else []
        self.citations = citations if citations else []
        self.notes = notes
        self.group = auto_assign_group(group, project)

    @beartype
    def add_citation(self, citation: Union[Citation, dict]):
        self._add_node(citation, "citations")

    @beartype
    def remove_citation(self, citation: Union[Citation, int]):
        self._remove_node(citation, "citations")
