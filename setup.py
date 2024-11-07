from setuptools import setup, find_packages

setup(
    name="test_analytics",
    version="0.1.0",
    author="Ben Smith",
    author_email="ben.s@meetcleo.com",
    description="A test analytics package",
    packages=find_packages(),
    install_requires=['numpy', 'pandas'],
)
