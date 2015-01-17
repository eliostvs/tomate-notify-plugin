#!/bin/env python

import os

from paver.easy import needs, path, sh
from paver.setuputils import install_distutils_tasks
from paver.tasks import task

install_distutils_tasks()

ROOT_PATH = path(__file__).dirname().abspath()

PLUGIN_PATH = ROOT_PATH / 'data' / 'plugins'

TOMATE_PATH = ROOT_PATH / 'tomate'


@needs(['test'])
@task
def default():
    pass


@task
def install():
    sh('cat packages.txt | sudo xargs apt-get -y --force-yes install')


@task
def clean():
    sh('pyclean data/plugin')
    sh('pyclean .')
    sh('rm .coverage', ignore_error=True)


@task
def test(options):
    os.environ['PYTHONPATH'] = '%s:%s' % (TOMATE_PATH, PLUGIN_PATH)
    sh('nosetests --cover-erase --with-coverage tests.py')


@task
def docker_build():
    sh('docker build -t eliostvs/tomate-notify-plugin .')


@task
def docker_run():
    sh('docker run --rm eliostvs/tomate-notify-plugin')
