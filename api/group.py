
import  maya.cmds as cmds


class Group(object):
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        
        # TODO: Ugly
        if not cmds.objExists(self.name):
            if parent:
                cmds.group(name=self.name, parent=self.parent, empty=True)
            else:
                cmds.group(name=self.name, empty=True)

    def group_nodes(self, *args):
        for argument in args:
            try:
                cmds.parent(argument, self.name)
            except:
                pass
    
    # TODO: Move this to parent class with support for cmds *args
    @property
    def children(self, all_descendents=True):
        return cmds.listRelatives(allDescendents=all_descendents)

    def set_visible(self, toggle=True):
        if toggle:
            cmds.hide(self.name)
        if not toggle:
            self.showHidden(self.name)
