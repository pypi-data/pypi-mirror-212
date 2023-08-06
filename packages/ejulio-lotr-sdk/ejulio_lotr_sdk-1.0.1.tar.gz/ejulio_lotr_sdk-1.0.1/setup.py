from setuptools import setup, find_packages


install_requires=['requests==2.31.0']


setup(
    name='ejulio_lotr_sdk',
    version='1.0.1',
    url='https://github.com/ejulio/julio-batista-sdk',
    author='Júlio César Batista',
    author_email='julio.batista@outlook.com',
    description='A SDK for The Lord of the Rings',
    long_description='A SDK for The Lord of the Rings',
    license='MIT',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires,
    tests_require=['requests', 'pytest', 'requests-mock'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ],
)