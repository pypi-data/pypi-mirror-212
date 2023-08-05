from setuptools import setup, find_packages

setup(name='module_client',
      version='1.0',
      description='module client',
      packages=find_packages(),
      author_email='shatdar@yandex.ru',
      author='Daria Shatilova',
      install_requeres=['PyQt5', 'sqlalchemy', 'pycruptodome', 'pycryptodomex']
      )
