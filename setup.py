
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
    python_requires='>=3.0',
    install_requires=['flask >=0.12', 'flask_sqlalchemy >=2.1']
)