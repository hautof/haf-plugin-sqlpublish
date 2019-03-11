import setuptools, os
from setuptools import setup

PACKAGE_NAME = "hafsqlpublish"


VERSION_MAIN = 0
VERSION_SUB = 0
VERSION_FIX = 2


requires = [
    'haf',
    'twine',
    'setuptools'
        ]


with open('ReadMe.md', encoding='utf8') as f:
    long_description = f.read()


def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            print(filename)
            paths.append(os.path.join('..', path, filename))
    return paths


setup(
    name = PACKAGE_NAME,
    version = f"{VERSION_MAIN}.{VERSION_SUB}.{VERSION_FIX}",
    author = 'wei.meng',
    author_email = 'mengwei1101@hotmail.com',    
    long_description = long_description,
    long_description_content_type='text/markdown',
    url='http://github.com/hautof/haf-plugin-webserver',
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    install_requires=requires,
    platforms='Posix; MacOS X; Windows',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)