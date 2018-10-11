from setuptools import setup

setup(
    name='snapshotTool',
    version='0.1',
    author='Florian Putker',
    author_email='putkerflorian@hotmail.com',
    description='Snapshot and instance manager for AWS',
    license='GNU',
    packages=['src'],
    url='https://github.com/Fputker/snapshotTool',
    install_requires=[
        'click',
        'boto3'
    ],
    entry_points='''
        [console_scripts]
        snapshotTool=src.main:cli
    ''',
)

