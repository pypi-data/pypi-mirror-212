from . import g_var


def set_log_level(debug_level):
    g_var.set_var(g_var.GVarKey.Log.LOG_LEVEL, debug_level)


def get_log_level():
    return g_var.get_var(g_var.GVarKey.Log.LOG_LEVEL)
