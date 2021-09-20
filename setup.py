from pathlib import Path

from setuptools import find_packages, setup

if __name__ == '__main__':
    with Path(Path(__file__).parent, 'README.md').open(encoding='utf-8') as file:
        long_description = file.read()

    with Path(Path(__file__).parent, 'requirements.txt').open(encoding='utf-8') as file:
        requirements = file.readlines()

    setup(
        name='smartdataset',
        packages=find_packages(),
        include_package_data=True,
        version='0.0.1a',
        license='MIT',
        description='A smart and efficent dataset, which builds as you train',
        long_description=long_description,
        long_description_content_type='text/markdown',
        entry_points={'console_scripts': [
            'smartdataset = smartdataset:master']},
        author='Aarush Katta',
        author_email='ARKsealplays@gmail.com',
        url='https://github.com/ARKseal/smartdataset',
        data_files=[('.', ['README.md', 'requirements.txt'])],
        keywords=['machine learning', 'computer vision',
                  'download', 'image', 'dataset'],
        install_requires=requirements,
        classifiers=[
            'Intended Audience :: Developers',
            'Topic :: Scientific/Engineering :: Artificial Intelligence',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3.6',
        ],
    )
