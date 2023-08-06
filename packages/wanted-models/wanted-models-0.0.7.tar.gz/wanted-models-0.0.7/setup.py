from setuptools import setup, find_packages

setup(
    name='wanted-models',
    version='0.0.7',
    packages=find_packages(),
    url='https://gitlab.argus360.kz/argus/kgp/wanted-models/',
    license='MIT',
    author='mercurial',
    author_email='dias.nespayev@gmail.com',
    description='Wanted models',
    python_requires=">=3.8",
    install_requires=['pydantic'],
)
