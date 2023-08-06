from setuptools import find_packages, setup

setup(
    name="yahalloLib",
    version="1.0.0",
    packages=find_packages(include=["yahalloLib", "yahalloLib.*"]),
    description="IGI LAB3",
    author="Daniil",
    entry_points={
        'console_scripts': ['yahalloLib=yahalloLib.lib:main']
    }
)
