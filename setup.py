from setuptools import setup, find_packages


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='googleapitoolkit',
      version='0.1',
      description='Toolkit for using GA and BigQuery',
      url='',
      author='',
      author_email='',
      license='MIT',
      packages=["base", "big_query", "google_analytics"],
      zip_safe=False)