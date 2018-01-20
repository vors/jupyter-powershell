from distutils.core import setup
setup(
  name = 'powershell_kernel',
  packages = ['powershell_kernel'],
  version = '0.0.2',
  description = 'PowerShell language kernel for Jupyter',
  author = 'Sergei Vorobev',
  author_email = 'xvorsx@gmail.com',
  url = 'https://github.com/vors/jupyter-powershell',
  download_url = 'https://github.com/vors/jupyter-powershell/archive/0.0.2.tar.gz',
  keywords = ['ikernel', 'jupyter', 'powershell', 'pwsh'],
  classifiers = [],
  package_data={'powershell_kernel': ['*', 'killableprocess/*.py']},
)
