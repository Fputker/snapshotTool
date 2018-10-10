from setuptools import setup

setup(
    name='snapshotTool',
    version='0.1',
    author='',
    author_email='',
    description='',
    license='',
    packages=['src'],
    url='https://github.com/Fputker/snapshotTool',
    install_requires=[
        'click',
        boto3
    ],
    entry_points=''''
        [console_scripts]
        snapshotTool=src.main:cli
    ''',
)

