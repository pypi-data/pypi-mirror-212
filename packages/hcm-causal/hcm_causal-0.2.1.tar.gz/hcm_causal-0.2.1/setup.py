from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    README = fh.read()

VERSION = '0.2.1'

setup(
    name='hcm_causal',
    version=VERSION,
    author='',
    description='hcm_causal Python Package',
    long_description=README,
    long_description_content_type='text/markdown',
    install_requires=[
        'numpy',
        'scipy',
        'pandas',
        'JPype1',
        'causal-learn',
        'python-igraph',
        'torch',
        'tqdm',
        'scikit-learn',
        'toolz',
        'bayesian-optimization >= 1.1.0'
    ],
    url='https://github.com/haharay/hcm_causal',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    scripts=['bin/notears_linear',
             'bin/notears_nonlinear'],
    packages=find_packages(),
    include_package_data=True,
    package_dir={'notears':'notears','dagma':'dagma','pytetrad':'pytetrad','synthdid':'synthdid'},
    python_requires='>=3.9',
)
