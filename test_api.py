import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify

from app import create_app
from database.models import setup_db, db_drop_and_create_all, Movie, Actor

# This test will delete all the rows in the db !! only use locally

# Auth tokens
assistant = (
    'bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IklJYl9yakw1TWdUT20zS3Z4R2ozNyJ9.eyJpc3MiOiJodHRwczovL2Rldi0yLXMtemIyai5ldS5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMTMyNjYyNTY5MDM1MzM3Mjc4MjkiLCJhdWQiOlsiY2Fwc3RvbmUiLCJodHRwczovL2Rldi0yLXMtemIyai5ldS5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNTk0NDcwMDk0LCJleHAiOjE1OTQ0NzcyOTQsImF6cCI6Im5jYTMyNmJYVXZZeFpIVmVEUGdERTB3THpOdXNaSm82Iiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.qoHZXvxet0hgQEq5UUSi5ai6U-cVSo4H5bjRhL8sFRKi7eBGww08aUZj6DCyOL-nxuycmCj1ppou36boLfGeiBe4h8EW2oghp0DqUvbXlkhC8vPbo28hhw07aJ4X9xXc58y9z4M392ZLJIwNCJxvC1lD7M2aGNuw0C767lO6Ne4GVGyy0iTs0mzUN8K8RfM8dpVBrynohSZb9uZg613vUN6NLszXBRV4hz2P-BzC9CldoMwjkcvBhFiFXyV3it6Ov0w7-KVx_GAPlkV4mS7jLOBn-sdanmoBZuASRvHXk0jSrD6A8AJfhzMuKLbGI9tCBIpH_W4aD1lI08_HNJLcaw'
)

director = (
    'bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IklJYl9yakw1TWdUT20zS3Z4R2ozNyJ9.eyJpc3MiOiJodHRwczovL2Rldi0yLXMtemIyai5ldS5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMTgxMjA2MTgzNzE5OTgxNzg5MjciLCJhdWQiOlsiY2Fwc3RvbmUiLCJodHRwczovL2Rldi0yLXMtemIyai5ldS5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNTk0NDcwMzkyLCJleHAiOjE1OTQ0Nzc1OTIsImF6cCI6Im5jYTMyNmJYVXZZeFpIVmVEUGdERTB3THpOdXNaSm82Iiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIl19.FOganV3Hq94xCGtZibqjiJBHSOk_gMBVEbNptNxIGU4FrJmaaQEC2Z3_kc8Z8R_-0HAFw2drhKXm8CWjpf-3jMCZdOpoMcXGzPC3isg694g4BQpY7i_vl58mNMDKLQReVo9y8qWd1qpF7uSyzeZFSnR1XuCIb-A0Yrc0VNReB4VBA2LMiV_lTONBdxJIFfwbUDeD7DSLzL9EAq_4Z9sdpEfiEufTd4nc1NpWN3cmbB3oUM4Ak14pMzS-PaIhS3o5XhybMKYSeexBASrW88Hau7ODyJPQeT-_7_LOAUL2HRRxNHcAtMSCIdvrUJ1SJ3GmdRL3r8AlqaN8IumaynOzQw'
)

producer = (
    'bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IklJYl9yakw1TWdUT20zS3Z4R2ozNyJ9.eyJpc3MiOiJodHRwczovL2Rldi0yLXMtemIyai5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVhZWVmNTdkYzMyMDYwYmU3ZjdmNmNkIiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE1OTQ0NzA1OTcsImV4cCI6MTU5NDQ3Nzc5NywiYXpwIjoibmNhMzI2YlhVdll4WkhWZURQZ0RFMHdMek51c1pKbzYiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.jwGj8g1Ta0ua9HNLo1Lsp562o_wZKZpcSJ3Cnclyeo6Fhx0Dsxy9QlKs8ne4gl5ZrSYotkFTI8KVnSDRj1EflOZ9Up_iIoWRMsHr5kPZqgaNT4xnLJ-SG1FRzLyDycldQUoMdDxQSTtY7dgjtPsNfyzeEVUqCWM_olwW5wg-ZqwVm5dkYkgaiGFi2dAsUWwq8pRMjm4AIKtVL5lc6PB60qa-Vuo4Y1A6q8ZqD5CKt7NgG0key3yCDAbFFDcrfNH7yKRsPdxiC7yqv-EJ2-eUZ9JXEJIJaRFVNu-YkGjFmUeDsF-KiZoLx_XgqlyxbRvJXqrHw3J9myOAFN1kCQYvfg'
)


class CastingTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = (
            'postgresql://postgres:Ioneryle1@localhost:5432/agency'
        )
        self.header_assistant = {
            'Content-Type': 'application/json',
            'Authorization': assistant
        }
        self.header_director = {
            'Content-Type': 'application/json',
            'Authorization': director
        }
        self.header_producer = {
            'Content-Type': 'application/json',
            'Authorization': producer
        }
        setup_db(self.app, self.database_path)

    def tearDown(self):
        pass

    def test_0_refresh_db(self):
        db_drop_and_create_all()

    def test_1_get_movies(self):
        # All roles can perform this function
        res = self.client().get('/movies', headers=self.header_assistant)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_2_get_actors(self):
        # All roles can perform this function
        res = self.client().get('/actors', headers=self.header_assistant)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_3_post_movies(self):
        # Only producer can perform this function
        new_movie = {
            "title": "love actually",
            "release_date": 20200428
        }
        res = self.client().post(
                    '/movies',
                    json=new_movie,
                    headers=self.header_producer
                )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_4_post_actors(self):
        # Director and producer can perform this function
        new_actor = {
            "name": "brad pitt",
            "age": 45,
            "gender": "male"
        }
        res = self.client().post(
                    '/actors',
                    json=new_actor,
                    headers=self.header_director
                )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_5_patch_movies(self):
        # Director and producer can perform this function
        patch_movie = {
            "title": "love actually",
            "release_date": 20190428
        }
        res = self.client().patch(
                    '/movies/1',
                    json=patch_movie,
                    headers=self.header_director
                )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_6_patch_actors(self):
        # Director and producer can perform this function
        patch_actor = {
            "name": "brad pitt",
            "age": 45,
            "gender": "female"
        }
        res = self.client().patch(
                    '/actors/1',
                    json=patch_actor,
                    headers=self.header_director
                )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_7_delete_movies(self):
        # Only producer can perform this function
        res = self.client().delete('/movies/1', headers=self.header_producer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_8_delete_actors(self):
        # Director and producer can perform this function
        res = self.client().delete('/actors/1', headers=self.header_director)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
