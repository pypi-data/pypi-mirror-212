import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='opentherm-web-api',
    author='Lake292',
    author_email='lake.erik@gmail.com',
    description='WebAPI Connector for OpenThermWeb',
    keywords='openthermweb',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Lake292/opentherm-web-api',
    project_urls={
        'Bug Reports': 'https://github.com/Lake292/opentherm-web-api/issues'
    },
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    classifiers=[
        # see https://pypi.org/classifiers/
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Developers',

        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
     install_requires=['requests'],
    extras_require={
        'dev': ['check-manifest'],
        # 'test': ['coverage'],
    }
)
