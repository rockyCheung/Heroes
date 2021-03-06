import io

from setuptools import find_packages, setup

with io.open('README.md', 'r', encoding='utf8') as f:
    readme = f.read()

setup(
    name='pursue',
    version='1.0.0',
    url='https://github.com/rockyCheung/Heroes',
    license='BSD',
    maintainer='Pallets team',
    maintainer_email='bigroc_ren@hotmail.com',
    long_description_content_type="text/markdown",
    description='pursue.',
    long_description=readme,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask','Click>=7.0','Flask-SQLAlchemy>=2.4.0','Jinja2>=2.10.1','MarkupSafe>=1.1.1','SQLAlchemy>=1.3.3','Werkzeug>=0.15.2'
        ,'pytest>=4.4.1','fbprophet>=0.5','plotly>=3.10.0','lxml==4.3.4'
    ],
    extras_require={
        'test': [
            'pytest',
            'coverage',
        ],
    },
)
