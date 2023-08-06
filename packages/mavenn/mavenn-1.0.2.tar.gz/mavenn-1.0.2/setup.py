from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='mavenn',
      version='1.0.2',
      description='MAVE-NN: genotype-phenotype maps from multiplex assays of variant effect',
      long_description=readme(),
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
      ],
      keywords='mave, mpa, global epistasis',
      url='http://mavenn.readthedocs.io',
      author='Ammar Tareen, Mahdi Kooshkbaghi, Justin B. Kinney',
      author_email='tareen@cshl.edu',
      license='MIT',
      packages=['mavenn'],
      include_package_data=True,
      install_requires=[
        'numpy<=1.23.5',
		'matplotlib>=3.2.0',
		'pandas>=1.3.0',
		'tensorflow>=2.0.0',
		'scikit-learn>=0.22',
		'logomaker>=0.8'
      ],
      zip_safe=False)