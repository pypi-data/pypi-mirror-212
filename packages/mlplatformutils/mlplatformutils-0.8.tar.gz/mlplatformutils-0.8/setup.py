from setuptools import setup, find_packages

setup(
    name='mlplatformutils',
    version='0.8',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3.8'
    ],
    author='Keshav Singh',
    author_email='keshav_singh@hotmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    keywords='mlplatformutils',
    install_requires=[
          'applicationinsights','gremlinpython','azureml-core'
      ],

)
