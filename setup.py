from setuptools import find_packages, setup

setup(
    name='flaskr',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Flask==2.2.3',
        'pytest==7.2.2',
        'Werkzeug==2.2.3',
        'setuptools==67.6.0'
    ],
)
