from setuptools import find_packages, setup


def read_file(file_name):
    with open(file_name) as f:
        return f.read()


setup(
    name="trigger-auto-tests",
    version=read_file("version.txt"),
    author="Kyrylo Maksymenko",
    author_email="saklar13@gmail.com",
    packages=find_packages(),
    entry_points={
        "console_scripts": ["trigger-auto-tests = trigger_auto_tests.cli:cli"]
    },
    include_package_data=True,
    install_requires=read_file("requirements.txt"),
    python_requires="~=3.7",
)
