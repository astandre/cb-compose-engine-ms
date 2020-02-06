from setuptools import setup, find_packages
from kbsbot.compose_engine import __version__

setup(name='compose-engine',
      description="This microservice is  intended to communicate with other services in order to determine intents and entities to retrieve the answer for the channel.",
      long_description=open('README.rst').read(),
      version=__version__,
      packages=find_packages(),
      zip_safe=False,
      include_package_data=True,
      dependency_links=["https://github.com/Runnerly/flakon.git#egg=flakon"],
      install_requires=["flask", "requests", "flask_sqlalchemy"],
      author="André Herrera",
      author_email="andreherrera97@hotmail.com",
      license="MIT",
      keywords=["chatbots", "microservices"],
      entry_points={
          'console_scripts': [
              'compose-engine = kbsbot.compose_engine.run:main',
          ],
      }
      )
