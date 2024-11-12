from setuptools import setup, find_packages

setup(
    name="test_analytics",
    version="0.1.1",
    author="Ben Smith",
    author_email="ben.s@meetcleo.com",
    description="A test analytics package",
    packages=find_packages(),
    install_requires=['numpy', 'pandas'],
    include_package_data=True,
    package_data={"test_analytics": ["queries/*.sql"]}
)
