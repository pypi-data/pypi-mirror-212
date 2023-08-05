from setuptools import setup, find_packages

setup(name='module_server',
      version='1.0',
      description='module server',
      packages=find_packages(),
      author_email='shatdar@yandex.ru',
      author='Daria Shatilova',
      install_requeres=['PyQt5', 'sqlalchemy', 'pycruptodome', 'pycryptodomex']
      )