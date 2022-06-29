import traceback
import os

#dbg = print
def dbg(msg):
    print("<pid:{0}>dbg:{1}".format(os.getpid(), msg))

def print_exception_info():
    # dbg(type(sys.exc_info()[1]))
    # dbg(sys.exc_info()[1])
    # dbg(sys.exc_info()[-1].tb_lineno)
    try:
        traceback.print_exc()
    except:
        pass
