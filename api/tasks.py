"""
(c) Copyright Jalasoft. 2023

tasks.py
    test todoist tasks endpoint using nose2
"""
import logging
import unittest

import requests

from api.todo_base import TodoBase
from config.config import HEADERS
from utils.logger import get_logger
from utils.rest_client import RestClient

LOGGER = get_logger(__name__, logging.DEBUG)


class Tasks(unittest.TestCase):
    """
    Tasks endpoints test using nose2
    """
    @classmethod
    def setUpClass(cls):
        cls.url_tasks = "https://api.todoist.com/rest/v2/tasks"
        cls.session = requests.Session()

        cls.project_id = TodoBase().get_all_projects()['body'][1]["id"]
        cls.section_id = TodoBase().get_all_sections()['body'][1]["id"]
        cls.task_id = TodoBase().get_all_tasks()['body'][1]["id"]

    def test_create_task(self):
        """
        Test Create Task
        """
        response = self.create_task()
        assert response['status'] == 200

    def test_create_task_with_project_id(self):
        """
        Test Create Task using project id
        """
        project_id = self.project_id
        response = self.create_task(project_id=project_id)
        assert response['status'] == 200

    def test_create_task_with_section_id(self):
        """
        Test Create Task using section id
        """
        section_id = self.section_id
        response = self.create_task(section_id=section_id)
        assert response['status'] == 200

    def test_get_all_tasks(self):
        """
        Test get all tasks
        """
        response = TodoBase().get_all_tasks()
        LOGGER.info("Number of tasks returned: %s", len(response['body']))
        assert response['status'] == 200

    def test_get_task_by_id(self):
        """
        Test get Task by id
        """
        task_id = self.task_id
        LOGGER.info("Task Id: %s", task_id)
        url_task = f"{self.url_tasks}/{task_id}"
        response = RestClient().send_request("get", session=self.session,
                                             headers=HEADERS, url=url_task)
        assert response['status'] == 200

    def test_close_task(self):
        """
        Test Close Task
        """
        task_id = self.task_id
        LOGGER.info("Task Id: %s", task_id)
        url_task_close = f"{self.url_tasks}/{task_id}/close"
        response = RestClient().send_request("post", session=self.session, headers=HEADERS,
                                             url=url_task_close)

        assert response['status'] == 204

    def test_reopen_task(self):
        """
        Test reopen Task
        """
        # valid task open
        task_id = self.create_task()['body']["id"]

        # close
        url_task_close = f"{self.url_tasks}/{task_id}/close"
        response_close = RestClient().send_request("post", session=self.session, headers=HEADERS,
                                                   url=url_task_close)

        assert response_close['status'] == 204

        LOGGER.info("Task Id: %s", task_id)
        url_task_reopen = f"{self.url_tasks}/{task_id}/reopen"
        response = RestClient().send_request("post", session=self.session, headers=HEADERS,
                                             url=url_task_reopen)

        assert response['status'] == 204

    def create_task(self, project_id=None, section_id=None):
        """
        Create Task request method
        """
        data = {
            "content": "Task inside section",
            "due_string": "tomorrow at 12:00",
            "due_lang": "en",
            "priority": 4
        }
        if project_id:
            data["project_id"] = project_id
        if section_id:
            data["section_id"] = section_id

        response = RestClient().send_request("post", session=self.session, headers=HEADERS,
                                             url=self.url_tasks, data=data)

        return response
