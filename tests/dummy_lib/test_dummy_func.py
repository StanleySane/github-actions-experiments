#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest

from dummy_lib.dummy_func import dummy_func


class TestDummyFunc(unittest.TestCase):

    def test_success(self):
        msg = 'Hello'
        expected_echo = f"Echo {msg!r}"

        echo = dummy_func(msg)

        self.assertEqual(echo, expected_echo)
