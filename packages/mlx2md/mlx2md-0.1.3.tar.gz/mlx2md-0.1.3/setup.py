from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='mlx2md',
    version='0.1.3',    
    description='Matlab mlx to Markdown format converter',
    url='https://github.com/alient12/mlx2md',
    author='Ali Entezari',
    author_email='ali_ent12@yahoo.com',
    license='BSD 2-clause',
    packages=['mlx2md'],
    long_description=readme(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)