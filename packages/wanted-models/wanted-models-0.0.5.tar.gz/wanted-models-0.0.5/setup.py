from setuptools import setup, find_packages

setup(
    name='wanted-models',
    version='0.0.5',
    packages=find_packages(),
    url='',
    license='MIT',
    author='mercurial',
    author_email='dias.nespayev@gmail.com',
    description='Wanted models',
    python_requires=">=3.8",
    install_requires=['pydantic'],
)
