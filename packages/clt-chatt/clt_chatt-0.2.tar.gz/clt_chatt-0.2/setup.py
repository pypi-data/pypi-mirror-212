from setuptools import setup, find_packages

setup(
    name="clt_chatt",
    version="0.2",
    description="Client packet",
    packages=find_packages(),  # ,Будем искать пакеты тут(включаем авто поиск пакетов)
    author_email="test@gmail.com",
    author="Aleksandr",
    install_requeres=["PyQt5", "sqlalchemy", "pycruptodome", "pycryptodomex"]
    ##зависимости которые нужно до установить
)
