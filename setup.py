
import blackbook
from setuptools import setup

setup(
    name='BlackBook',
    version=blackbook.__version__,
    url='https://github.com/ievans3024/BlackBook',
    license='MIT',
    author=blackbook.__author__,
    description='A contact management application',
    test_suite='tests.test_all',
    install_requires=['Flask >=0.12', 'Flask-SQLAlchemy >=2.1', 'Flask-Script >=2.0.5']
)