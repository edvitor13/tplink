from setuptools import setup

setup(
    name='tplink',
    version='0.3.0b1',
    author='Vitor Gabriel',
    author_email='edvitor13@hotmail.com',
    packages=['tplink'],
    python_requires='>=3.11',
    install_requires=[
        'python-kasa>=0.6.2.1'
    ],
)
