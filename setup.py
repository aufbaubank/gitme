import gitme
from setuptools import setup
import setuptools

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='gitme',
    version=gitme.__version__,
    description='create merge requests on gitlab, based on changes already done',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='http://github.com/aufbaubank/gitme',
    author='Daniel Henneberg',
    author_email='daniel.henneberg@aufbaubank.de',
    license='MIT',
    entry_points={
        'console_scripts': ['gitme=gitme.entrypoint:main'],
    },
    zip_safe=False,
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    install_requires=[
        'requests',
        'GitPython'
    ],
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.8'
    ],
)
