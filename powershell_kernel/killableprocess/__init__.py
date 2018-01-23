from powershell_kernel.killableprocess.killableprocess import Popen, mswindows
if mswindows:
	from powershell_kernel.killableprocess.winprocess import STARTUPINFO, STARTF_USESHOWWINDOW