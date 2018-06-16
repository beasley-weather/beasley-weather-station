from setuptools import setup


setup(
    name='beasley-weather-station',
    author='francium',
    packages=['transfer_system'],
    license='MIT',
    include_package_data=True,
    install_requires=[
        'marshmallow-sqlalchemy',
        'sqlalchemy',
        'sqlalchemy-utils',
    ]
)
