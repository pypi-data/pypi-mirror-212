from setuptools import setup, find_packages

setup(name='mess_server_dima_pro',
      version='0.1',
      description='Server packet',
      packages=find_packages(),  # ,Будем искать пакеты тут(включаем авто поиск пакетов)
      author_email='dima_protasevich92@mail.ru',
      author='Dima Protasevich',
      install_requeres=['PyQt5', 'sqlalchemy', 'pycruptodome', 'pycryptodomex']
      # зависимости которые нужно до установить
      )