import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdktf-gke-auth",
    "version": "1.1.0",
    "description": "cdktf-gke-auth",
    "license": "Apache-2.0",
    "url": "https://github.com/01walid/cdktf-gke-auth.git",
    "long_description_content_type": "text/markdown",
    "author": "Walid Ziouche<hi@walid.dev>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/01walid/cdktf-gke-auth.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdktf_gke_auth",
        "cdktf_gke_auth._jsii"
    ],
    "package_data": {
        "cdktf_gke_auth._jsii": [
            "cdktf-gke-auth@1.1.0.jsii.tgz"
        ],
        "cdktf_gke_auth": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.7",
    "install_requires": [
        "cdktf-cdktf-provider-google>=7.0.0, <8.0.0",
        "cdktf>=0.16.0, <0.17.0",
        "constructs>=10.2.0, <10.3.0",
        "jsii>=1.82.0, <2.0.0",
        "publication>=0.0.3",
        "typeguard~=2.13.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
