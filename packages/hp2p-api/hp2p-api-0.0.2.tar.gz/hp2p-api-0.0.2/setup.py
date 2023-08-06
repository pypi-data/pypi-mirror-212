from setuptools import setup, find_packages

setup(
    name='hp2p-api',
    version='0.0.2',
    description='An API for HP2P Peer',
    author='JAYB',
    author_email='jaylee@jayb.kr',
    url='https://github.com/ITU-T-SG11-Q8/Q.4102',
    install_requires=['grpcio', 'grpcio-tools', 'protobuf',],
    packages=find_packages(exclude=[]),
    keywords=['hp2p', 'hp2p-api'],
    python_requires='>=3.8',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
    ],
)
