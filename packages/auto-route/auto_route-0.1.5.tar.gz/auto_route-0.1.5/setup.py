from setuptools import setup, find_packages

setup(
    name='auto_route',
    version='0.1.5',  # Semantic Versioning
    packages=["auto_route", "auto_app"],
    author='Ruben Fernandez',
    author_email='ruben@carbonyl.org',
    description="Thank you for your interest in contributing to the AutoRoute project! Our goal is to simplify and "
                "automate the creation of SaaS/PaaS solutions. We're excited to welcome you to our community.",
    long_description=open('README.rst').read(),
    long_description_content_type='text/x-rst',
    url='https://github.com/Bucanero06/auto_route',
    install_requires=[
        "fastapi",
        "pydantic",
        "uvicorn",
    ],
)
