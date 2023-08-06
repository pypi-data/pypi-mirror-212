# -*- coding: UTF-8 -*-
# @Time    : 2022/9/5 23:38
# @File    : __init__.py
# @Author  : jian<jian@mltalker.com>
from __future__ import division
from __future__ import unicode_literals
from __future__ import print_function
from antgo.pipeline.hub import *
import os

def run(project, folder='./deploy', **kwargs):
    project_folder = os.path.join(folder, f'{project}_plugin')
    if not os.path.exists(project_folder):
        print(f'Project {project} not exist.')
        return

    os.system(f'cd {project_folder} && bash run.sh')

def package(project, folder='./deploy', **kwargs):
    # project_folder = os.path.join(folder, f'{project}_plugin')
    # if not os.path.exists(project_folder):
    #     print(f'Project {project} not exist.')
    #     return

    # os.system(f'cd {project_folder} && bash package.sh')
    pass


def service(project, folder='./deploy', **kwargs):
    pass