import setuptools

from pathlib import Path

import glob

# note: build this package with the following command:
# .

base_path = Path(__file__).parent
long_description = (base_path / 'README.md').read_text()

setuptools.setup(
    name='screen-html',
    version='0.1.0',
    author='Xpos587',
    license='MIT',
    description='This is a Python script that uses Playwright to render HTML and convert it into an image.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    python_requires='>=3.7',
    packages=['screen_html'],
    # package_dir={
    #     '': 'screen_html'
    # },
    include_package_data=True,
    # py_modules=['screen_html'],
    install_requires=['Jinja2', 'playwright'],
    url='https://github.com/Xpos587/screen-html'
)
