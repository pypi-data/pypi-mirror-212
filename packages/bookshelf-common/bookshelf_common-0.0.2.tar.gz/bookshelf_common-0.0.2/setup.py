from setuptools import setup, find_packages

VERSION = '0.0.2'
DESCRIPTION = 'Share common code for bookshelf'
LONG_DESCRIPTION = 'This package will share some of the common code that we use for implementation of  bookshelf micro services.'

# Setting up
setup(
    name="bookshelf_common",
    version=VERSION,
    author="Marko Muric",
    author_email="<atis.443@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url='https://github.com/mmuric/bookshelf-common',
    packages=find_packages(),    
    project_urls = {
        "Bug Tracker": "https://github.com/mmuric/bookshelf-common/issues"
    },
    license='MIT',    
)