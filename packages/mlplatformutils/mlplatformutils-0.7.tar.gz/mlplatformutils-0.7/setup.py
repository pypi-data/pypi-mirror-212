from setuptools import setup, find_packages
import os
directory = os.getcwd()

with open(directory+"/README.md") as f:
    long_description = f.read()

setup(
    name='mlplatformutils',
    long_description=long_description,
    long_description_content_type='text/markdown',
    version='0.7',
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
