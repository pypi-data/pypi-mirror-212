import setuptools
from pathlib import Path

setuptools.setup(
    name='gymPanda-env',
    version='1.0.3',
    description="A OpenAI Gym Env for Panda arm",
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(include="gym_panda_env*"),
    install_requires=['gym']  # And any other dependencies foo needs
)

