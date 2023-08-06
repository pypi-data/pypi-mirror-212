from setuptools import setup, find_packages

with open("README.md", "r") as rd:
  long_description = rd.read()

setup(
 name='ezlab',
 version='0.0.1',
 description='A python package that helps you manage files in Google Colab notebooks.',
 url='https://github.com/pratik-tan10/ezlab', 
 author='Pratik Dhungana',
 author_email='pdhungana@crimson.ua.edu',
 classifiers=[
   'Development Status :: 4 - Beta',
   'Intended Audience :: Developers',
   'Operating System :: OS Independent',
   'License :: OSI Approved :: MIT License',
   'Programming Language :: Python :: 3',
   'Programming Language :: Python :: 3.5',
   'Programming Language :: Python :: 3.6',
   'Programming Language :: Python :: 3.7',
   'Programming Language :: Python :: 3.8',
 ],
 install_requires=[
  ],
 keywords=['python', 'ezlab', 'colab'],
 packages=find_packages(),
 long_description=long_description,
 long_description_content_type="text/markdown"
)