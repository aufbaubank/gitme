import gitme
from setuptools import setup
import setuptools

setup(
    name='gitme',
    version=gitme.__version__,
    description='create merge requests on gitlab, based on changes already done',
    url='http://github.com/aufbaubank/smerger',
    author='Daniel Henneberg',
    author_email='daniel.henneberg@aufbaubank.de',
    license='MIT',
    entry_points={
        'console_scripts': ['gitme=gitme.entrypoint:main'],
    },
    zip_safe=False,
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    install_requires=['requests']
)
