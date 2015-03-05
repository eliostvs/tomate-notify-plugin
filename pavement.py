#!/bin/env python
import os

from paver.easy import needs, path, sh
from paver.tasks import task

ROOT_PATH = path(__file__).dirname().abspath()

PLUGIN_PATH = ROOT_PATH / 'data' / 'plugins'

TOMATE_PATH = ROOT_PATH / 'tomate'


@task
@needs(['test'])
def default():
    pass


@task
def test(options):
    os.environ['PYTHONPATH'] = '%s:%s' % (TOMATE_PATH, PLUGIN_PATH)
    sh('nosetests --cover-erase --with-coverage tests.py')


@task
def clean():
    sh('pyclean data/plugin')
    sh('pyclean .')
    sh('rm .coverage', ignore_error=True)


@task
@needs(['docker_rmi', 'docker_build', 'docker_run'])
def docker_test():
    pass


@task
def docker_rmi():
    sh('docker rmi eliostvs/tomate-notify-plugin', ignore_error=True)


@task
def docker_build():
    sh('docker build -t eliostvs/tomate-notify-plugin .')


@task
def docker_run():
    sh('docker run --rm eliostvs/tomate-notify-plugin')
