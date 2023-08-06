from setuptools import setup,find_namespace_packages
from os import listdir
setup(name='smper',

      version='5.1',

      url='https://github.com/parlorsky/sempaiper',

      license='MIT',

      author='Levap Vobayr',

      author_email='tffriend015@gmail.com',

      description='',
      packages=find_namespace_packages(where="src"),
      package_dir={"": "src"},
      package_data={},
      zip_safe=False)
