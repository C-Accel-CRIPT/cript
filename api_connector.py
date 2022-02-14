"""
CRIPT REST API Connector
"""
import requests
import json
from typing import Union
from getpass import getpass

from beartype import beartype
from beartype.typing import Type
from pprint import pprint

from . import node_classes
from .nodes import Base
from .errors import APIAuthError, APIRefreshError, APISaveError, APISearchError


class API:
    @beartype
    def __init__(self, url: str):
        """
        Establishes a session with the CRIPT API.

        :param url: The API endpoint URL.
        """
        self.url = url.rstrip("/")
        self.session = requests.Session()
        token = getpass("API Token: ")

        self.session.headers = {
            "Authorization": token,
            "Content-Type": "application/json",
        }

        # Test API connection
        try:
            self.session.get(self.url)
        except requests.exceptions.ConnectionError as e:
            print(e)

        # Test API authentication
        response = self.session.get(self.url)
        if response.status_code == 401:
            raise APIAuthError(response.json()["detail"])

        # Print success message
        print(f"\nConnection to the API was successful.\n")

    def __repr__(self):
        return f"Connected to {self.url}"

    def __str__(self):
        return f"Connected to {self.url}"

    @beartype
    def refresh(self, node: Base):
        """
        Overwrite a node's attributes with the latest values from the DB.

        :param node: The node to refresh.
        """
        if hasattr(node, "url"):
            if node.url:
                response = self.session.get(node.url)
                self._set_node_attributes(node, response.json())
                node.print_json()
            else:
                raise APIRefreshError(
                    "Before you can refresh a node, you must either save it or define it's URL."
                )
        else:
            raise APIRefreshError(
                f"{node.name} is a secondary node, thus cannot be refreshed."
            )

    @beartype
    def save(self, node: Base):
        """
        Save or update a node in the DB.

        :param node: The node to be saved.
        """
        if node.node_type == "primary":
            if node.url:
                response = self._update(node)
            else:
                response = self._create(node)
            if response.status_code in (200, 201):
                self._set_node_attributes(node, response.json())
                node.print_json()
            else:
                pprint(response.json())
        else:
            raise APISaveError(
                "The save() method cannot be called on secondary node such as {node.name}"
            )

    def _create(self, node):
        """
        Send a JSON POST request to the API.

        :param node: The node to be created.
        :return: The HTTP response object.
        """
        if node.slug == "file":
            headers = {"Authorization": self.session.headers["Authorization"]}
            file = {"file": open(node.source, "rb")}
            return self.session.post(
                url=f"{self.url}/{node.slug}/", headers=headers, files=file, data={}
            )
        else:
            return self.session.post(
                url=f"{self.url}/{node.slug}/", data=json.dumps(node.to_dict())
            )

    def _update(self, node):
        """
        Send a JSON PUT request to the API.

        :param node: The node to be updated.
        :return: The HTTP response object.
        """
        if node.slug == "file":
            headers = {"Authorization": self.session.headers["Authorization"]}
            file = {"file": open(node.source, "rb")}
            return self.session.put(
                url=node.url, headers=headers, files=node.file, data={}
            )
        else:
            return self.session.put(url=node.url, data=json.dumps(node.to_dict()))

    def _set_node_attributes(self, node, response_json):
        """
        Set node attributes using data from an API response.

        :param node: The node you want to set attributes for.
        :param response: The response from an API call.
        """
        for json_key, json_value in response_json.items():
            attr_value = getattr(node, json_key)
            if (
                isinstance(json_value, str)
                and self.url in json_value
                and json_key != "url"
            ):
                continue
            elif isinstance(json_value, dict):
                self._set_node_attributes(attr_value, json_value)
            else:
                setattr(node, json_key, json_value)

    @beartype
    def get(self, url: str):
        """
        Get the JSON for a node and use it to generated a local node object.

        :param url: The API URL of the node.
        :return: The generated node object.
        """
        # Define node class from URL slug
        node_slug = url.rstrip("/").rsplit("/")[-2]
        node_class = None
        for node_cls in node_classes:
            if hasattr(node_cls, "slug") and node_cls.slug == node_slug:
                node_class = node_cls

        if self.url not in url or node_class is None:
            raise APISearchError("Please enter a valid node URL.")

        response = self.session.get(url)
        if response.status_code == 200:
            response_json = response.json()

            created_at = response_json.pop("created_at", None)
            updated_at = response_json.pop("updated_at", None)

            node = node_class(**response_json)
            node.created_at = created_at
            node.updated_at = updated_at

            return node
        else:
            raise APISearchError(f"The specified {node_class.name} node was not found.")

    @beartype
    def search(self, node_class: Type[Base], query: dict = None):
        """
        Send a query to the API and print the results.

        :param node: The node type you want to search.
        :param query: A dictionary defining the query parameters.
        """
        if node_class.node_type == "secondary":
            raise APISearchError(
                f"{node_class.name} is a secondary node, thus cannot be searched."
            )
        if isinstance(query, dict):
            query_slug = self._generate_query_slug(query)
            response = self.session.get(f"{self.url}/{node_class.slug}/?{query_slug}")
        elif query is None:
            response = self.session.get(f"{self.url}/{node_class.slug}/")
        else:
            raise APISearchError(f"'{query}' is not a valid query.")

        pprint(response.json())

    def _generate_query_slug(self, query):
        """Generate the query URL slug."""
        slug = ""
        for key in query:
            slug += f"{key}={query[key]}&"
        return slug
