# image_compress
 compress image before save

# Create package
    # create setup.py
    ``
    from setuptools import setup, find_packages

    setup(
        name='image_compress',
        version='0.4',
        description='A sample image compress',
        long_description='Test Long',
        author='ReimiBeta',
        author_email='reimi846@gmail.com',
        url='https://github.com/reimibeta',
        license='MIT',
        packages=find_packages(),
        # py_modules=['image_compress',],
        install_requires=[
            # other dependencies
            'Pillow'
        ],
        # other optional arguments
    )
    ``
    # build and create dist folder
    python setup.py build 
    python setup.py sdist 
    # install twine
    pip3 install twine
    # upload project
    twine upload --repository pypi dist/*
    # note it may error because of name already exist