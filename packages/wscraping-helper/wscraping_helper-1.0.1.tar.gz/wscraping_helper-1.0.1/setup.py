from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='wscraping_helper',
    version='1.0.1',
    description='WebScraping helper module',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Komáromi János',
    author_email='komaromijano2002@gmail.com',
    packages=['wscraping_helper'],
    install_requires=[
        "requests",
    ]
)