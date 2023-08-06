from setuptools import find_packages, setup
setup(
    name='dheedemo',
    packages=find_packages(),
    version='0.1.0',
    description='Dhee observability client',
    author='Datalens',
    setup_requires=['pytest-runner'],
    tests_require=['pytest==6.2.5'],
    install_requires=["requests"],
    test_suite='tests',
)
