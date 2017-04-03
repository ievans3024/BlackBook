
import blackbook
from setuptools import setup

setup(
    name="BlackBook",
    version=blackbook.__version__,
    url="https://github.com/ievans3024/BlackBook",
    license="MIT",
    author=blackbook.__author__,
    description="A contact management application",
    test_suite="tests.test_all"
)