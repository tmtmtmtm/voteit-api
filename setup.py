import os
from setuptools import setup, find_packages

setup(
    name='voteit-api',
    version='0.2',
    description="voteit API server",
    long_description="",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
    keywords='votes parliament',
    author='CodeCamp',
    author_email='tony@micropiphany.com',
    url='',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=[],
    include_package_data=True,
    zip_safe=False,
    install_requires=[],
    entry_points={},
    tests_require=[],
    test_suite=''
)
