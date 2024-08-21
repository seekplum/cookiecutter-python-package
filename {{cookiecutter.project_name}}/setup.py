from setuptools import find_packages, setup


def install():
    setup(
        setup_requires=[],
        include_package_data=True,
        packages=find_packages(exclude=["tests", "docs"]),
    )


def init():
    pass


if __name__ == "__main__":
    install()
    init()
