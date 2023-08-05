from setuptools import setup, find_packages

setup(
    name='zakupki-saver-models',
    version='0.0.1',
    packages=find_packages(),
    url='',
    license='MIT',
    author='mercurial',
    author_email='dias.nespayev@gmail.com',
    description='Zakupki saver models',
    python_requires=">=3.5",
    install_requires=['pydantic'],
)
