"""
(c) Copyright Jalasoft. 2023

comments.py
    test todoist comments endpoint using nose2
"""
import logging
import unittest

import requests

from api.todo_base import TodoBase
from config.config import HEADERS
from utils.logger import get_logger
from utils.rest_client import RestClient

LOGGER = get_logger(__name__, logging.INFO)


class Comments(unittest.TestCase):
    """
    Comments endpoints test using nose2
    """
    @classmethod
    def setUpClass(cls):
        cls.url_comments = "https://api.todoist.com/rest/v2/comments"
        cls.session = requests.Session()

        cls.task_id = TodoBase().get_all_tasks()['body'][1]["id"]
        cls.comment_id = TodoBase().get_all_comments(cls.task_id)['body'][0]["id"]

    def test_create_task(self):
        """
        Test Create Task
        """
        LOGGER.info("Creating comment under : %s", self.task_id)
        response = self.create_comment("Content for test create comment", self.task_id)
        assert response['status'] == 200

    def test_get_all_comments(self):
        """
        Test get all comments
        """
        response = TodoBase().get_all_comments(self.task_id)
        LOGGER.info("Number of comments returned: %s", len(response['body']))
        assert response['status'] == 200

    def test_get_comment_by_id(self):
        """
        Test get comment by id
        """
        comment_id = self.comment_id
        LOGGER.info("Comments Id to search comment by ID: %s", comment_id)
        url = f"{self.url_comments}/{comment_id}"
        response = RestClient().send_request("get", session=self.session,
                                             headers=HEADERS, url=url)
        assert response['status'] == 200

    def test_update_coment(self):
        """
        Test update Comment
        """
        # valid comment to update
        comment_id = self.create_comment("Content for test update comment",
                                         self.task_id)['body']['id']
        update_data = {"content": "Updated comment"}
        LOGGER.info("Comment Id to update: %s", comment_id)
        url = f"{self.url_comments}/{comment_id}"
        response = RestClient().send_request("post", session=self.session, headers=HEADERS,
                                             url=url, data=update_data)

        assert response['status'] == 200

    def test_delete_task(self):
        """"
        Tet delete task
        """
        # valid comment to update
        comment_id = self.create_comment("  Content for test delete comment",
                                         self.task_id)['body']['id']
        LOGGER.info("Comment Id to delete: %s", comment_id)
        url = f"{self.url_comments}/{comment_id}"
        response = RestClient().send_request("delete", session=self.session, headers=HEADERS,
                                             url=url)
        assert response['status'] == 204

    def create_comment(self, content, task_id):
        """
        Create Task request method
        """
        data = {
            "task_id": task_id,
            "content": content,

        }
        response = RestClient().send_request("post", session=self.session, headers=HEADERS,
                                             url=self.url_comments, data=data)

        return response
