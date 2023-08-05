from setuptools import setup
from setuptools.command.install import install


class CustomInstallCommand(install):
    def run(self):
        # Place your custom commands here
        print("Running custom commands during installation")

        from dotenv import load_dotenv
        load_dotenv()

        # Call the original install command
        install.run(self)


with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", 'r') as r:
    requirements = r.read().splitlines()

with open("LICENSE.txt", 'r') as l:
    license = l.read()

setup(
    name="genetikaplusIO",
    version="0.0.2",
    author="Alon Ben Zion",
    author_email="alon@genetikaplus.com",
    license=license,
    description="IO for database",
    py_modules=["gp_db_io", "gp_storage_io", "gp_sqlconnection"],
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    cmdclass={
        'install': CustomInstallCommand,
    },
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=requirements
)
