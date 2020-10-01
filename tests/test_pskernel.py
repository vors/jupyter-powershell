import unittest
import jupyter_kernel_test as jkt

# Test file that is made to test PowerShell Kernel Info and Test Cases
class PowerShellKernelTests(jkt.KernelTests):
    # The name identifying an installed kernel to run the tests against
    kernel_name = "PowerShell"

    # language_info.name in a kernel_info_reply should match this
    language_name = "powershell"

    file_extension = ".ps1"

 
    # Code in the kernel's language to write "hello, world" to stdout
    code_hello_world = "Write-Host 'hello, world'"

    # Code Execute Result should be used to do test cases
    code_execute_result = [
        # Test for Write Command
        {'code': 'Write-Host Hello', 'result': 'Hello'},
        # Test for Interactive Streaming Support
        {'code': 'For ($i=0; $i -le 3; $i++) { echo \"Hello\" Start-Sleep 1}', 'result': 'Hello\nHello\nHello\nHello\n'},
        # # Test for Large String Streaming Support
        {'code': 'For ($i=0; $i -le 1; $i++) { echo ("test" * 20) Start-Sleep 1}', 'result': 'testtesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttest\ntesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttest\n'},
    ]
    

if __name__ == '__main__':
    unittest.main()