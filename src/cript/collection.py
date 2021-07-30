"""
Collection Node

"""

from .base import BaseModel
from .utils.type_check import *

class Collection(BaseModel):

    _class = "Collection"

    def __init__(
        self,
        name: str,
        c_collections=None,
        notes: str = None
    ):
        """
        :param name: The name of the collection.

        :param c_collections:

        :param notes: Any miscellaneous notes related to the user.
        :param _class: class of node.
        :param uid: The unique ID of the material.
        :param model_version: Version of CRIPT data model.
        :param version_control: Link to version control node.
        :param last_modified_date: Last date the node was modified.
        :param created_date: Date it was created.
        """
        super().__init__(name=name, _class=self._class, notes=notes)


        #child collectinos
        #experiments