from distutils.core import setup

from setuptools import find_packages


def readme():
    """print long description"""
    with open('README.md') as f:
        return f.read()


setup(
    name='thumbor_hsl',
    version='0.0.3',
    packages=find_packages(),
    url='https://github.com/BowlingX/thumbor-http-stats-loader',
    license='MIT',
    author='David Heidrich',
    author_email='me@bowlingx.com',
    install_requires=['thumbor>=7.0.0a2,<8'],
    description='A modified `http` loader for thumbor which provides additional statistics '
                '(like width, height and url parsing)',
    long_description=readme(),
)
