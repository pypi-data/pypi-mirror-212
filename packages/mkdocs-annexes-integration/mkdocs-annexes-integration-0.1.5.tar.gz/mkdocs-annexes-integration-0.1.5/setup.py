import io

from setuptools import setup, find_packages

setup(
    name='mkdocs-annexes-integration',
    version='0.1.5',
    description='A MkDocs plugin transforming annexes files into images or code blocks to be integrated in markdown pages',
    long_description=io.open('readme.md', encoding='utf8').read(),
    long_description_content_type='text/markdown',
    keywords='mkdocs',
    url='https://gitlab.com/cfpt-mkdocs-plugins/mkdocs-annexes-integration',
    author='Thibaud Briard',
    author_email='thibaud.brrd@eduge.ch',
    license='MIT',
    python_requires='>=3.8',
    install_requires=[
        'mkdocs>=1.4.2',
        'pdf2image>=1.16.3'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
    ],
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'mkdocs.plugins': [
            'annexes-integration = mkdocs_annexes_integration.plugin:AnnexesIntegration'
        ]
    }
)