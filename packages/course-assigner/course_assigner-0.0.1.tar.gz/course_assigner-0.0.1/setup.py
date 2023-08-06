from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='course_assigner',
    packages=find_packages(),
    version='0.0.1',
    author='Wesley Belleman',
    author_email="bellemanwesley@gmail.com",
    description="Assign students to classes based on preference.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bellemanwesley/course_assigner",
    license='MIT',
    #install_requires=["numpy"],
    #setup_requires=['pytest-runner'],
    #tests_require=['pytest==4.4.1'],
    #test_suite='tests',
    #classifiers=[
    #    "Development Status :: 5 - Production/Stable",
    #    "Programming Language :: Python :: 3",
    #    "License :: OSI Approved :: MIT License",
    #    "Operating System :: OS Independent",
    #],
    python_requires='>=3.10',
)