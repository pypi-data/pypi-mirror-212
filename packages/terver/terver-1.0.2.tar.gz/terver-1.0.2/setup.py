from setuptools import setup, find_packages

def readme():
  with open('README.md', 'r') as f:
    return f.read()

setup(
  name='terver',
  version='1.0.2',
  author='qdzzzxc',
  author_email='nikitstp@gmail.com',
  description='xD',
  long_description=readme(),
  long_description_content_type='text/markdown',
  packages=find_packages(),
  install_requires=['pyperclip>=1.8.2'],
  classifiers=[
    'Programming Language :: Python :: 3.7',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='example python',
  python_requires='>=3.7'
)