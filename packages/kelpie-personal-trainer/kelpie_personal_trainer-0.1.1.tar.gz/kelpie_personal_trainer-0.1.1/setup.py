from setuptools import setup, find_packages

VERSION = '0.1.1'
DESCRIPTION = 'Personal Trainer Library'

# Setting up
setup(
    name="kelpie_personal_trainer",
    version=VERSION,
    author="Ariel",
    author_email="<arillesmana2001@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['pandas', 'opencv-python', 'pickle', 'mediapipe', 'numpy'],
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
