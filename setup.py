import sys
from setuptools import setup, find_packages
from kbsbot.compose_engine import __version__

with open('requirements.txt') as f:
    deps = [dep for dep in f.read().split('\n') if dep.strip() != ''
            and not dep.startswith('-e')]
    install_requires = deps

setup(name='compose-engine',
      description="",
      long_description=open('README.rst').read(),
      version=__version__,
      packages=find_packages(),
      zip_safe=False,
      include_package_data=True,
      install_requires=install_requires,
      author="André Herrera",
      author_email="andreherrera97@hotmail.com",
      license="MIT",
      keywords=["chatbots", "microservices", "linked data"],
      entry_points={
          'console_scripts': [
              'compose-engine = kbsbot.compose_engine.run:app',
          ],
      }
      )
