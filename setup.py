""" Setup.py file for bipy package
"""
from setuptools import setup

setup(
    name="bipy",
    version="0.1.0",
    author="Ajeet Singh",
    author_email="singajeet@gmail.com",
    packages=["bipy", "bipy.services", "bipy.services.db", "bipy.services.db.analytic",
              "bipy.services.db.connection_managers", "bipy.services.db.repository",
              "bipy.services.db.warehouse", "bipy.services.db.warehouse.browsers",
              "bipy.services.db.warehouse.base_meta_gen", "bipy.services.decorators",
              "bipy.services.security"
             ],
    url="https://github.com/singajeet/bipy",
    license="LICENSE.txt",
    description="Python based BusinessIntelligence application",
    long_description=open('README.txt').read(),
    install_requires=["yapsy", "sqlalchemy", "Config", "logging", "json", "os"]
)
