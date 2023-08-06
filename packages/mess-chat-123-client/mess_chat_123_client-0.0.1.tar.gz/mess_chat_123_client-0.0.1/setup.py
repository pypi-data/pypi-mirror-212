from setuptools import setup, find_packages

setup(name="mess_chat_123_client",
      version="0.0.1",
      description="message_client",
      author="Natalia Pisarova",
      author_email="natalia@yandex.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
