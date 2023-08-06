from setuptools import find_packages, setup

setup(
    name="anchorconnector",
    packages=find_packages(include=["anchorconnector"]),
    version="0.3.0",
    description="Anchor Connector for Podcast Data",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Open Podcast",
    license="MIT",
    entry_points={
        "console_scripts": [
            "anchorconnector = anchorconnector.__main__:main",
        ]
    },
    install_requires=["requests", "loguru", "PyYAML", "tenacity"],
)
