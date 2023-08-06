from distutils.core import setup
setup(
  name = 'remlalib',
  packages = ['remlalib'],
  version = open("remlalib/_version.py").readlines()[-1].split()[-1].strip("\"'"),
  license='MIT',
  description = 'REMLA23 - Team 13 - Lib',
  long_description= 'REMLA23 - Team 13 - Lib',
  author = 'Team 13',
  author_email = 'gasparsantosrocha@gmail.com',
  url = 'https://github.com/remla23-team13/lib',
  download_url = 'https://github.com/remla23-team13/lib',
  keywords = ['REMLA', 'Versioning'],
  install_requires=[
      'setuptools'
  ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.1',
    'Programming Language :: Python :: 3.2',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)