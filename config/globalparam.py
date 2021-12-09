#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os

config_file_path = os.path.split(os.path.realpath(__file__))[0]
project_path = os.path.join(config_file_path, '..')
report_path = os.path.join(project_path, 'report', 'testreport')
log_path = os.path.join(project_path, 'report', 'log')
if not os.path.isdir(log_path):
    os.makedirs(log_path)
server_path = os.path.join(config_file_path, 'server.yaml')
case_path = os.path.join(project_path, 'testcase')
base_path = os.path.join(project_path, 'public', 'base')
