import contextlib
import maya.cmds as cmds

@contextlib.contextmanager
def unlocked_attr(attr):
    """
    Unlock a locked attr, and then lock it again

    with unlocked_attr(attr.focalLength):
        attr.focalLength.set(33)
    """
    is_locked = attr.isLocked()
    try:
        attr.unlock()
        yield attr
    finally:
        if is_locked:
            attr.lock()


@contextlib.contextmanager
def chunk_undo():
    cmds.undoInfo(openChunk=True)
    yield
    cmds.undoInfo(closeChunk=True)


class undo_off(object):
    """
    Turn off undo inside context manager

    Keyword Args:
        flush (bool): Whether or not to delete the previous undo queue 
        before the command. (Defaults to True)
    """

    def __init__(self, flush=True):
        self.flush = flush

    def __enter__(self):
        self.undo_state = cmds.undoInfo(query=True, state=True)
        if self.undo_state:
            if not self.flush:
                cmds.undoInfo(stateWithoutFlush=False)
            else:
                cmds.undoInfo(state=False)

    def __exit__(self, *_):
        if self.undo_state:
            if not self.flush:
                cmds.undoInfo(stateWithoutFlush=True)
            else:
                cmds.undoInfo(state=True)


class chunk_undo_and_undo(object):
    @staticmethod
    def _close_and_undo(defer=False):
        do_undo = not cmds.undoInfo(undoQueueEmpty=True, query=True)
        cmds.undoInfo(closeChunk=True)
        if do_undo:
            if defer and not cmds.about(batch=True):
                cmds.evalDeferred("cmds.undo()")
            else:
                cmds.undo()

    def __enter__(self):
        cmds.undoInfo(openChunk=True)

    def __exit__(self, *_):
        self._close_and_undo()

