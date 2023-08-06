from setuptools import setup, find_packages

setup(
    name="dfmodule_DSTemplate",
    version="0.0.4",
    description="dfmodule for DE -> DS code transition",
    author="SG, JH",
    author_email="rimmoyee@example.com",
    url="https://github.com/Data-Flower/dfmodule_DSTemplate",
    install_requires=['boto3', 'pandas', 'python-dotenv', 'requests', 'dfmodule'],
    packages=find_packages(exclude=['tests*']),
    keywords=['dfmodule_DS, dfmodule, dfmodule_DSTemplate'],
    python_requires='>=3.6',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    license="",
)