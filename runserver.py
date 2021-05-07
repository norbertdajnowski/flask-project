#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from project import app
import dotenv

if __name__ == '__main__':
    CONFIG = dotenv.dotenv_values()
    port = int(os.environ.get("PORT", 5017))
    app.run("localhost", port=port)
