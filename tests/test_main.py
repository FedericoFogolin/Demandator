#! /usr/bin/env python3

import unittest
from demandator_pkg import db_handler
import os


class TestMain(unittest.TestCase):

    def setUp(self):
        # note: this would be better done with tempfile
        db_handler.open_or_create(0)
        db_handler.save_new_username('enrico', 'enrico', 0)

    def test_wrong_username(self):
        user = db_handler.check_for_username('andrea', 'andrea', 2)
        self.assertFalse(user)

    def test_correct_username(self):
        user = db_handler.check_for_username('enrico', 'enrico', 2)
        self.assertTrue(user)

    def tearDown(self):
        os.remove('./user_pwd.db')
