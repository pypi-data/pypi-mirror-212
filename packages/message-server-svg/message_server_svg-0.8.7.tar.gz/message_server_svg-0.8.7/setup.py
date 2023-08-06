from setuptools import setup, find_packages

setup(name="message_server_svg",
      version="0.8.7",
      description="message_server",
      author="Sergey Grishin",
      author_email="svg95@lsit.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
