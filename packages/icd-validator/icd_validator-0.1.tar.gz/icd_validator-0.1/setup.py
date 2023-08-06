from setuptools import setup, find_packages

setup(
    name='icd_validator',
    version='0.1',
    author="JeeAnRyu",
    description="icd 9 and 10 code validator with regular expression",
    license="MIT",
    keywords="ICD910, ICD-9, ICD-10, medical coding, validation, healthcare",
    packages=["icd_validator"],
    install_requires=['pandas'],
)

