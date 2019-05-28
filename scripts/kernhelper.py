from __future__ import print_function

import lldb

# This flag is set when ptrace PT_DENY_ATTACH is called
P_LNOATTACH = '0x00001000'

# This function assumes that your connected to the XNU kernel and have loaded
# the XNU helper function showalltasks
def show_ptrace_deny_attach_procs():
    ci = lldb.debugger.GetCommandInterpreter()
    
    tasks = lldb.SBCommandReturnObject()
    ci.HandleCommand('showalltasks', tasks)

    for item in tasks.GetOutput().split('\n'):
        if item[0:4] == 'task':
            continue

        proc = item[84:102].strip()
        name = item[130:].strip()

        lflag = lldb.SBCommandReturnObject()
        ci.HandleCommand('po ((struct proc *)%s)->p_lflag & %s' % (proc, P_LNOATTACH), lflag)
        
        if lflag is None or lflag.GetOutput() is None:
            continue

        if lflag.GetOutput().strip() != '0':
            print(proc + ': ' + name)
