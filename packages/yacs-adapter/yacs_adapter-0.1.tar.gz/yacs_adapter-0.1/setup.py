from setuptools import setup, find_packages

setup(
    name='yacs_adapter',
    version='0.1',
    description='An adapter for YACS to improve readability and usability',
    author='codexquantum',
    author_email='karllorentzcodex@outlook.com',
    url='https://github.com/codexquantum/YACS_Adapter',
    packages=find_packages(),
    install_requires=[
        'yacs',
    ],
    entry_points = {
        'console_scripts': ['yacs_sync= sync.sync:main'],
    },
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
)