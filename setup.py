from setuptools import setup, find_packages

setup(
    name="pyzohocrm",  # Replace with your package name
    version="0.1.4",
    description="A Basic Zoho Crm utility Package with Token Management",
    author="Rahul Kumar",
    author_email="rahul.work.programming@gmail.com",
    url="https://github.com/rahul-08-11/pyzohocrm",
    packages=find_packages(),
    install_requires=[],  # Add dependencies if needed
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)