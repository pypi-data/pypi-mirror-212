from setuptools import setup

setup(name='threatmon',
      version='0.0.1',
      description='Easy to use, open source computer vision library for python',
      long_description='Easy to use, open source computer vision library for python',        
      url='https://threatmon.io/',
      author='Nurettin Sinanoğlu',
      author_email='nurettin.sinanogluu@gmail.com',
      license='MIT',
      packages=['threatmon'],
      include_package_data=True,
      zip_safe=False,
      install_requires=['numpy', 'progressbar', 'requests', 'pillow', 'imutils']
      )