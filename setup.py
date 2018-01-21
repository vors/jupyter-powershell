from distutils.core import setup
setup(
  name = 'powershell_kernel',
  packages = ['powershell_kernel'],
  version = '0.0.5',
  description = 'PowerShell language kernel for Jupyter',
  author = 'Sergei Vorobev',
  author_email = 'xvorsx@gmail.com',
  url = 'https://github.com/vors/jupyter-powershell',
  keywords = ['ikernel', 'jupyter', 'powershell', 'pwsh'],
  classifiers = [],
  package_data={'powershell_kernel': ['*', 'killableprocess/*.py']},
)
