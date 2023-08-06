import setuptools

with open('ReadMe.md', 'r') as fl:
    long_description = fl.read()

setuptools.setup(
    name='Translinguer',
    version='0.0.3',
    author='AivanF.',
    author_email='projects@aivanf.com',
    description='Allows writing simple scripts to manage locale/translation files',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/AivanF/Translinguer',
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Topic :: Utilities',
        'Topic :: Text Processing',
        'License :: Freely Distributable',
    ],
)
