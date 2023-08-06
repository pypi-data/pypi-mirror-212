from setuptools import setup, find_packages

VERSION = '0.2.17'
DESCRIPTION = 'Personal Trainer Library'


# Setting up
setup(
    name="kelpie_personal_trainer",
    version=VERSION,
    author="Ariel",
    author_email="<arillesmana2001@gmail.com>",
    long_description=open('README.md').read(),
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    package_data={
        'kelpie_personal_trainer': ['models/*']
    },
    include_package_data=True,
    install_requires=['scikit-learn', 'pandas', 'opencv-python', 'mediapipe', 'numpy', 'tensorflow', 'keras', 'matplotlib'],
    keywords=['python'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
