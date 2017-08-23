from ctypes import *
from my_debugger_define import *

Kernel32=windll.Kernel32

class debugger():
    def __init__(self):
        pass

    def load(self,path_to_exe):
        creation_flags=DEBUG_PROCESS

        startupinfo=STARTUPINFO()
        process_information=PROCESS_INFORMATION

        startupinfo.dwFlags=0x1
        startupinfo.wShowWindow=0x0

        startupinfo.cb=sizeof(startupinfo)


        if Kernel32.CreateProcessA(path_to_exe,
                                   None,
                                   None,
                                   None,
                                   None,
                                   creation_flags,
                                   None,
                                   None,
                                   byref(startupinfo),
                                   byref(process_information)):
            print "[*] we have successfully launched the process!"
            print "[*]PID: %d " % process_information.dw

        else:
            print "[*] Error: 0x%08x. " %Kernel32.GetLastError()
