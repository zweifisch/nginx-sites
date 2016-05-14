from setuptools import setup

setup(
    name='nginx-sites',
    url='https://github.com/zweifisch/nginx-sites',
    version='0.1.6',
    description='cli utility for managing nginx site configs',
    author='Feng Zhou',
    author_email='zf.pascal@gmail.com',
    packages=['nginx_sites'],
    package_data={'nginx_sites': ['templates/*.conf']},
    install_requires=['docopt', 'pystache'],
    entry_points={
        'console_scripts': ['nginx-sites=nginx_sites:main',
                            'ngx=nginx_sites:main'],
    },
)
