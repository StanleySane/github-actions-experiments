#!/usr/bin/python
# -*- coding: utf-8 -*-
""" Dummy functions
"""

import logging

logging.getLogger().addHandler(logging.NullHandler())


def dummy_func(msg: str) -> str:
    logging.info(f"Inside dummy_func with {msg!r}")

    return f"Echo {msg!r}"
