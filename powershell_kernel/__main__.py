from IPython.kernel.zmq.kernelapp import IPKernelApp
from .kernel import PowerShellKernel
IPKernelApp.launch_instance(kernel_class=PowerShellKernel)
