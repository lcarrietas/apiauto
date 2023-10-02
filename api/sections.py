"""
(c) Copyright Jalasoft. 2023

sections.py
    test todoist sections endpoint using nose2
"""
import logging
import unittest

import requests

from api.todo_base import TodoBase
from config.config import HEADERS
from utils.logger import get_logger
from utils.rest_client import RestClient

LOGGER = get_logger(__name__, logging.DEBUG)


class Sections(unittest.TestCase):
    """
    Section endpoints test using nose2
    """
    @classmethod
    def setUpClass(cls):
        cls.url_section = "https://api.todoist.com/rest/v2/sections"
        cls.session = requests.Session()

        cls.project_id = TodoBase().get_all_projects()['body'][1]["id"]

    def test_create_section(self):
        """
        Test to create session
        :return:
        """
        data = {
            "project_id": self.project_id,
            "name": "Test Create Section"
        }
        response = RestClient().send_request("post", session=self.session, headers=HEADERS,
                                             url=self.url_section, data=data)
        assert response["status"] == 200

    def test_get_all_sections(self):
        """
        Get all sections
        """
        response = TodoBase().get_all_sections()
        LOGGER.info("Number of sections returned: %s", len(response['body']))
        assert response["status"] == 200

    def test_get_all_sections_by_project(self):
        """
        Get all sections by project
        """
        if self.project_id:
            url_section = f"{self.url_section}?project_id={self.project_id}"

        response = RestClient().send_request("get", session=self.session, headers=HEADERS,
                                             url=url_section)
        LOGGER.info("Number of sections returned: %s", len(response))
        assert response["status"] == 200

    def test_get_section(self):
        """
        Get section by id
        """
        response = TodoBase().get_all_sections()
        section_id = response['body'][0]["id"]
        LOGGER.info("Section Id: %s", section_id)
        url_section = f"{self.url_section}/{section_id}"
        response = RestClient().send_request("get", session=self.session, headers=HEADERS,
                                             url=url_section)
        assert response["status"] == 200

    def test_update_section(self):
        """
        test update section
        """
        section_created = self.create_section('Vscode section')
        section_id = section_created["body"]["id"]
        data_update = {
            "name": "Udated Vscode Section"
        }
        url = f"{self.url_section}/{section_id}"
        response = RestClient().send_request("post", session=self.session, url=url,
                                             headers=HEADERS, data=data_update)
        assert response["status"] == 200

    def create_section(self, name_section):
        """
        Create project aux method
        """
        data = {
            "project_id": self.project_id,
            "name": name_section
        }
        response = RestClient().send_request("post", session=self.session, url=self.url_section,
                                             headers=HEADERS, data=data)
        return response

    def test_delete_section(self):
        """
        test delete section
        """
        section_created = self.create_section('section to delete')
        section_id = section_created["body"]["id"]
        url = f"{self.url_section}/{section_id}"
        response = RestClient().send_request("delete", session=self.session, url=url,
                                             headers=HEADERS)
        assert response["status"] == 204
