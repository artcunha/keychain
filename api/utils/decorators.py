"""
General decorators for Maya
"""
import functools

import maya.cmds as cmds

def ensure_unique_window(name):
    """
    Ensure that existing windows are destroyed before a new one is craeted.
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if cmds.window(name, exists=True):
                cmds.deleteUI(name)

            wsname = name + "WorkspaceControl"
            if cmds.workspaceControl(wsname, ex=True):
                if cmds.workspaceControlState(wsname, ex=True):
                    cmds.workspaceControlState(wsname, remove=True)
                cmds.deleteUI(wsname)

            return func(*args, **kwargs)

        return wrapper

    return decorator


def ensure_maya_initialized(func):
    """
    Decorator that ensure we are running in a initialized standalone
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not hasattr(cmds, "about"):
            from maya import standalone

            standalone.initialize()

        return func(*args, **kwargs)

    return wrapper


def single_undo(func):
    """Decorator for undo chunk.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        """Wraps the function.
        """
        try:
            cmds.undoInfo(openChunk=True)
            return func(*args, **kwargs)
        except Exception as e:
            raise e
        finally:
            cmds.undoInfo(closeChunk=True)

    return wrapper
