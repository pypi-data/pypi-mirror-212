from setuptools import setup, find_packages


setup(
    name="StreletsSerializer",
    version="1.0",
    description="module for python serialization(JSON, XML)",
    author="IGI",
    author_email="testeee@mail.ru",
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent"
    ],
    packages=["serializers"],
    include_package_data=True
)
