
from fabric.api import run

class RepoManager(object):
    def __init__(self):
        return

    @classmethod
    def repokey(cls, url):
        run("""
URL="%s"

""" % url)

    @classmethod
    def install(cls, package_name):
        run("""
PACKAGE_NAME="%s"

""" % package_name)

    @classmethod
    def remove(cls, package_name):
        run("""
PACKAGE_NAME="%s"

""" % package_name)

