from setuptools import setup, find_packages

with open('README.md', 'r') as fl :
    long_description = fl.read()

setup(
        # the name must match the folder name 'verysimplemodule'
        name="ArverRubika", 
        version='2.0.1',
        author="Aboli Coder",
        author_email="mirzaiabolfazl6@gmail.com",
        description='Coding the robot in Rubika in the easiest way !',
        long_description=long_description,
        long_description_content_type= 'text/markdown',
        packages=find_packages(),
        
        # add any additional packages that 
        # needs to be installed along with your package.
        install_requires=["pycryptodome==3.16.0", "Pillow==9.4.0"], 
        
        keywords=['python', 'rubel', 'Rubika', 'ArverRubika', 'robika', 'robot', 'ArseinRubika', 'arsein', 'arver', 'Arver', 'pyrubi'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
        ]
)
