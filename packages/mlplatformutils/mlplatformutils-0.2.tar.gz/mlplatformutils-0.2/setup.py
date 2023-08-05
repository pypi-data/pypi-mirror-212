from setuptools import setup, find_packages


setup(
    name='mlplatformutils',
    version='0.2',
    license='MIT',
    author='Keshav Singh',
    author_email='keshav_singh@hotmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    keywords='mlplatformutils',
    install_requires=[
          'applicationinsights','gremlinpython','azureml-core','adlfs','delta-lake-reader[azure]','pyarrowfs-adlgen2','pandas','azure-identity'
      ],

)
