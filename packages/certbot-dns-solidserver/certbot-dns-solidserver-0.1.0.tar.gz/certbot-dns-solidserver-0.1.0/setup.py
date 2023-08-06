from setuptools import setup, find_packages

version = "0.1.0"

install_requires = [
    "acme>=0.29.0",
    "certbot>=0.34.0",
    "eiprest",
    "setuptools",
]

# read the contents of your README file
with open("README.md") as f:
    long_description = f.read()

setup(
    name="certbot-dns-solidserver",
    version=version,
    description="SOLIDserver DNS Authenticator plugin for Certbot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/charlyhong/certbot-dns-solidserver",
    author="Charles Hong",
    author_email="ch@efficientip.com",
    license="Apache License 2.0",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Plugins",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Security",
        "Topic :: System :: Installation/Setup",
        "Topic :: System :: Networking",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
    ],

    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    entry_points={
        "certbot.plugins": [
            "dns-solidserver = certbot_dns_solidserver.dns_solidserver:Authenticator"
        ]
    },
    #test_suite="certbot_dns_solidserver",
)
