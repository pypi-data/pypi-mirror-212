from setuptools import setup, find_packages

setup(
    name='jhOMR',
    version='0.0.4',
    description='OMR format to be used in KUET',
    packages=find_packages(),
    install_requires=['numpy','pandas','opencv-python','openpyxl'],
    author='Md Nur Kutubul Alam',
    author_email='alamjhilam@gmail.com'
)