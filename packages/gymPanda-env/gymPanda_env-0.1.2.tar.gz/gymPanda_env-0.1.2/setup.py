import setuptools
from pathlib import Path

setuptools.setup(
    name='gymPanda_env',
    version='0.1.2',
    description="A OpenAI Gym Env for Panda arm",
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(include="gymPanda_env*"),
    install_requires=['gym']  # And any other dependencies foo needs
)

