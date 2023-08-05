from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Python serializer'
LONG_DESCRIPTION = 'Python serializer for lab 3'

# Setting up
setup(

    name="Serializer_CuteHedgehog",
    version=VERSION,
    author="Yulia Atrashonok",
    author_email="<yulia.atrashonok@yandex.ru>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=["Serializer"],

    keywords=['python', 'first package'],
    classifiers=[
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    include_package_data=True
)