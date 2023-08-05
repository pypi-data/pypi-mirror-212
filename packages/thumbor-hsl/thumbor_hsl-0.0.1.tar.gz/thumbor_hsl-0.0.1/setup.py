from distutils.core import setup

from setuptools import find_packages


def readme():
    """print long description"""
    with open('README.md') as f:
        return f.read()


setup(
    name='thumbor_hsl',
    version='0.0.1',
    packages=find_packages(),
    url='https://github.com/BowlingX/thumbor-http-header-stats-loader',
    license='MIT',
    author='David Heidrich',
    author_email='me@bowlingx.com',
    install_requires=['thumbor>=7.0.0a2,<8'],
    description='A modified `http` loader for thumbor which introduces an additional statd counter to track headers',
    long_description=readme(),
)
