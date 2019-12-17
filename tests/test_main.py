#! /usr/bin/env python3

import unittest
import os
from demandator_pkg import db_handler


class TestMain(unittest.TestCase):

    def setUp(self):
        db_handler.open_or_create(0, './user-pwd_test.db')
        db_handler.save_new_username('enrico', 'enrico', 0)
        db_handler.open_database(0, './user-pwd_test.db')

    def test_wrong_username(self):
        user = db_handler.check_for_username('abcd', 'abcd', 0)
        self.assertFalse(user)

    def test_correct_username(self):
        user = db_handler.check_for_username('enrico', 'enrico', 0)
        self.assertTrue(user)

    def tearDown(self):
        os.remove('./user-pwd_test.db')
