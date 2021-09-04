"""
User Node

"""

from . import CRIPTError
from .base import BaseModel, BaseReference
from .utils.validator.type_check import type_check_property
from .utils.validator.user import email_format_check, phone_format_check, orcid_format_check


class UserError(CRIPTError):
    def __init__(self, *msg):
        super().__init__(*msg)


class User(BaseModel):
    _class = "User"
    _error = UserError

    def __init__(
            self,
            name: str,
            email: str,
            phone: str = None,
            website: str = None,
            twitter: str = None,
            orcid: str = None,
            organization: str = None,
            position: str = None,
            c_group: list = None,
            c_publication: list = None,
            notes: str = None,
            **kwargs
    ):
        """

        :param name: The name of the user.
        :param email: The email id of the user.

        :param phone: The telephone number of the user.
        :param website: The personal website of the user.
        :param twitter: The Twitter handle of the user.
        :param orcid: The ORCID (https://orcid.org/) iD of the user.
        :param organization: The organization the user belongs to.
        :param position: The position/title of the user in their organization.

        :param c_group: CRIPT group you belong to

        :param notes: Any miscellaneous notes related to the user.
        :param _class: class of node.
        :param uid: The unique ID of the material.
        :param model_version: Version of CRIPT data model.
        :param version_control: Link to version control node.
        :param last_modified_date: Last date the node was modified.
        :param created_date: Date it was created.
        """

        super().__init__(name=name, _class=self._class, notes=notes, **kwargs)

        self._email = None
        self.email = email

        self._phone = None
        self.phone = phone

        self._website = None
        self.website = website

        self._twitter = None
        self.twitter = twitter

        self._orcid = None
        self.orcid = orcid

        self._organization = None
        self.organization = organization

        self._position = None
        self.position = position

        self.c_group = BaseReference("Group", c_group)
        self.c_publication = BaseReference("Publication", c_publication)

    @property
    def email(self):
        return self._email

    @email.setter
    @email_format_check
    @type_check_property
    def email(self, email):
        self._email = email

    @property
    def phone(self):
        return self._phone

    @phone.setter
    @phone_format_check
    @type_check_property
    def phone(self, phone):
        self._phone = phone

    @property
    def website(self):
        return self._website

    @website.setter
    @type_check_property
    def website(self, website):
        self._website = website

    @property
    def twitter(self):
        return self._twitter

    @twitter.setter
    @type_check_property
    def twitter(self, twitter):
        self._twitter = twitter

    @property
    def orcid(self):
        return self._orcid

    @orcid.setter
    @orcid_format_check
    @type_check_property
    def orcid(self, orcid):
        self._orcid = orcid

    @property
    def organization(self):
        return self._organization

    @organization.setter
    @type_check_property
    def organization(self, organization):
        self._organization = organization

    @property
    def position(self):
        return self._position

    @position.setter
    @type_check_property
    def position(self, position):
        self._position = position
