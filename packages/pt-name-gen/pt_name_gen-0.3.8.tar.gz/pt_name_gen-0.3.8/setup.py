from setuptools import setup

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='pt_name_gen',
    version='0.3.8',
    author='Victor Figueredo',
    author_email='cto@filterfeed.com.br',
    description='A name generator in Portuguese, with support to gender classification. Um gerador de nomes em português, com suporte para classificação de gênero.',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    install_requires=['unidecode'],
    python_requires='>=3.6',
    packages=['pt_name_gen'],
    include_package_data=True,
    package_data={
        "pt_name_gen": ["*.csv"]
    }
)
