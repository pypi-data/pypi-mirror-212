from setuptools import setup, find_packages

setup(
    name='gtci',
    packages=find_packages(),
    include_package_data=True,
    version="0.1.0",
    description='A GTCI installer is a command line tool that quickly and efficiently installs software and libraries while managing software dependencies. It\'s essential for deployment and development pipelines and automates the installation process.',
    long_description="An installer for GTCI (command line installer) is a useful tool that allows developers, beginners, and system administrators to install software and libraries from the command line interface quickly and efficiently. These installers use package managers to manage software dependencies and ensure a seamless installation process. They simplify the installation process and are an essential tool for deployment or development pipelines, particularly for automating installation processes. gtci installers are highly valuable in ensuring correct installation of software dependencies to prevent delays in the pipeline.",
    long_description_content_type="text/markdown",
    author='MR_GT',
    author_email='friendyt89@gmail.com',
    url='https://github.com/GreyTechno/gtci',
    keywords=['installer', 'gtci', 'cli', 'greytechno', 'mr_gt', 'packagemanagers', 'dependencies', 'automation', 'deploymentpipeline'],
    classifiers=[
            'Development Status :: 4 - Beta',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3',
            'Operating System :: OS Independent',
            'Environment :: Console',
    ],
    install_requires=["requests", "random2", "tqdm"],
    license='MIT',
    entry_points={
            'console_scripts': [
                'gtci = gtci.main:Main',
            ],
    },
    python_requires='>=3.5'
)
