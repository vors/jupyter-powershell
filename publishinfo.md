# Powershell kernel release

## Bump the version in the following locations:
- https://github.com/vors/jupyter-powershell/blob/261bcd5f73dac852042f8e8ff1518e39fbbd3d08/powershell_kernel/__init__.py#L2
- https://github.com/vors/jupyter-powershell/blob/261bcd5f73dac852042f8e8ff1518e39fbbd3d08/powershell_kernel/kernel.py#L14
- https://github.com/vors/jupyter-powershell/blob/261bcd5f73dac852042f8e8ff1518e39fbbd3d08/setup.py#L5

## Update Changelog
- Add descriptive content to describe what's new in latest version
## Create GitHub release

## Configure .pypirc File
Docs for how to setup .pypirc file can be found here: https://docs.python.org/3.6/distutils/packageindex.html#the-pypirc-file.
Note: it should look something like the following, and live in th $HOME directory. For security reasons, omit the password field, like so (you'll be prompted later for it when running sdist upload, don't worry!):

```[distutils]
index-servers =
  pypi

[pypi]
repository: https://pypi.python.org/pypi
username: <your_username_here>
```

## Install setup tools dependencies
pip install -U setuptools

## Edit setup.py
- Get latest in branch
- In setup.py, add the following under url:

  download_url = <path to tar.gz file in github release>,

example: https://github.com/vors/jupyter-powershell/archive/0.1.0.tar.gz

## Upload bits to pypi
python setup.py sdist upload -r pypi
