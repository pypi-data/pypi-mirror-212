from distutils.core import setup
from setuptools import find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(name='zoo-framework',  # 包名
      version='0.4.2',  # 版本号
      description='A simple and quick multi-threaded framework',
      long_description_content_type="text/markdown",
      long_description=long_description,
      author='XiangMeng',
      author_email='mengxiang931015@live.com',
      install_requires=["click","jinja2","gevent"],
      license='Apache License',
      packages=find_packages(),
      platforms=["all"],
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Topic :: Software Development :: Libraries'
      ],
      entry_points={
          'console_scripts': ['zfc = zoo_framework.__main__:zfc']
      }
)
