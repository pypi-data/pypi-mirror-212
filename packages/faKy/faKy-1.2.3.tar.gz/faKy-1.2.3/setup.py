from setuptools import setup

with open('readme.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='faKy',
    version='1.2.3',
    description='Your library description',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Sandro Barres Hamers',
    author_email='sbarreshamers@gmail.com',
    packages=['faKy'],
    install_requires=[
        'numpy==1.24.2',
        'spacy==2.3.9',
        'pandas==1.3.4',
        'spacy-readability==1.4.1',
        'nltk==3.7',
        'vaderSentiment==3.3.2',
    ],
    extras_require={
        'vader': ['vaderSentiment'],
        'en': ['en_core_web_md'],
    },
)
