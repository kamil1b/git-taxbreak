import setuptools

INSTALL_REQUIRES = ["gitpython"]

setuptools.setup(
    name="git-taxbreak",
    use_scm_version=True,
    install_requires=INSTALL_REQUIRES,
    setup_requires=["setuptools-scm", "setuptools>=40.0"],
    package_dir={"": "src"},
)
