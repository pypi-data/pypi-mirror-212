from setuptools import setup, find_packages

setup(
    name='django_admin_image_render',
    version='1.0.0',
    description='django render image for admin list',
    long_description='django render image for admin list',
    author='ReimiBeta',
    author_email='reimi846@gmail.com',
    url='https://github.com/reimibeta/django_admin_image_render',
    license='MIT',
    packages=find_packages(),
    # py_modules=['image_compress',],
    install_requires=[
        # other dependencies
        'Django==4.1.7',
    ],
    # other optional arguments
)
