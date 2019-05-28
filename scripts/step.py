from __future__ import print_function

import lldb

# This class will single step until the next call assembly instruction
# and then print out all the arguement registers
class Call:
    def __init__(self, thread_plan, dict):
        self.thread_plan = thread_plan

    def explains_stop(self, event):
        # We are stepping, so if we stop for any other reason, it isn't
        # because of us.        
        if self.thread_plan.GetThread().GetStopReason() == lldb.eStopReasonTrace:
            return True
        else:
            return False

    def should_stop(self, event):
        target = self.thread_plan.GetThread().GetProcess().GetTarget()
        frame = self.thread_plan.GetThread().GetFrameAtIndex(0)
        address = frame.GetPCAddress()

        insn = target.ReadInstructions(address, 1)[0]

        if 'call' in insn.GetMnemonic(target).lower():
            arg0 = frame.FindRegister('rdi').GetValue()
            arg1 = frame.FindRegister('rsi').GetValue()
            arg2 = frame.FindRegister('rdx').GetValue()
            arg3 = frame.FindRegister('rcx').GetValue()
            arg4 = frame.FindRegister('r8').GetValue()
            arg5 = frame.FindRegister('r9').GetValue()

            print('%s %s %s %s %s %s' % (arg0, arg1, arg2, arg3, arg4, arg5))
            self.thread_plan.SetPlanComplete(True)
            return True
        else:
            return False
    
    def should_step(self):
        # Whether to set the program running freely, or to instruction-single-step
        # the current thread. We always want to step
        return True