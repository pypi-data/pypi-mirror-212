from setuptools import setup, find_packages

setup(
    name='jhOMR',
    version='0.0.1',
    description='OMR format to be used in KUET',
    packages=find_packages(),
    install_requires=['numpy','pandas','cv2'],
    author='Md Nur Kutubul Alam',
    author_email='alamjhilam@gmail.com'
)