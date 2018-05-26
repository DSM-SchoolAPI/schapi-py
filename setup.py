from setuptools import setup

setup(
    name='schapi',
    version='1.1',
    url='https://github.com/DSM-SchoolAPI/schapi-py',
    license='Apache License 2.0',
    author='PlanB',
    author_email='mingyu.planb@gmail.com',
    description='Korean School meal API',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    packages=['schapi'],
    install_requires=['bs4', 'aiohttp']
)
