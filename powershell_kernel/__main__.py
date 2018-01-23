from IPython.kernel.zmq.kernelapp import IPKernelApp
from powershell_kernel.kernel import PowerShellKernel
IPKernelApp.launch_instance(kernel_class=PowerShellKernel)
