from setuptools import setup, find_packages

setup(
    name='FranAI',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'tinydb',
        'discord',
        'python-dotenv',
        'feedparser',
        'requests'
    ],
)
