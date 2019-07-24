from setuptools import setup, find_packages

with open('readme.md') as f:
    long_description = f.read()

setup(
    name='fortimail',
    version='0.1.0',
    description='Fortimail Rest API Client',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(exclude=['requirements', 'tests', ]),
    author_email='stephenh@startmail.com',
    python_requires='>=3.6',
    install_requires=['requests', ],
    author='surfer190',
    url='https://github.com/surfer190/fortimail.git',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English'
    ]
)
