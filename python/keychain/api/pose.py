import datetime
import enum
import json
import logging
import maya.cmds as cmds
import maya.OpenMaya as om

from keychain.api import anim_curve

LOGGER = logging.getLogger(__name__)

class State(enum.IntEnum):
    LOCAL = 0
    UNSYNCED = 1
    SYNCED = 2


class AnimBlock(object):
    """
    Container for animCurves
    """
    @classmethod
    def from_file(cls, filepath):
        anim_file = cls.get_anim_from_file(filepath)

        anim_block = cls(anim_curves=anim_file.get("data", None))
        # Save the rest of the file with the metadata, so that we can revert/compare
        anim_block._loaded_file = anim_file
        anim_block._filepath = filepath
        return anim_block

    def __init__(self, anim_curves=None):
        self.anim_curves = anim_curves
        self._loaded_file = None
        self._filepath = None
        self._state = State.LOCAL

    def apply(self):
        for node in self.nodes:
            anim_curve.set_node_anim_data(node, self.anim_curves)
        
    @property
    def nodes(self):
        return self.anim_curves.keys()


    @property
    def state(self):
        return self._state

    def check_state(self, filepath=None):
        # Add a better check for these two
        if not self._loaded_file or not self.filepath:
            self._state = State.LOCAL

        # TODO custom exception
        filepath = filepath or self.filepath
        anim_file = AnimBlock.get_anim_from_file(filepath)
        file_timestamp = anim_file.get("timestamp", None)

        diff = self.timestamp - file_timestamp
        
        if diff.seconds:
            set_synced(False)
        else:
            set_synced()

        return self.state
    
    def set_synced(self, synced=True):
        self._state = State.SYNCED if synced else State.UNSYNCED

    def export_to_file(self, filepath, anim_curves=None):
        anim_curves = anim_curves or self.anim_curves
        dump_dict = {
            "timestamp":self._get_timestamp(),
            "data":anim_curves,
        }
        with open(filepath, "w") as file_write:
            json.dump(dump_dict, file_write, indent=4)
    
    @property
    def timestamp(self):
        if self._loaded_file:
            return self._loaded_file.get("timestamp", None)
        LOGGER.info("Local block doesn't contain a timestamp as it hasn't been exported.")

    def _get_timestamp(self):
        return datetime.datetime.now().isoformat()

    # def _time_convert(time):
    #     if isinstance(time, datetime.datetime):
    #         return time.__str__()
        
    def load(self, filepath):
        anim_curves = get_anim_from_file(filepath)
        self.anim_curves = anim_curves
    
    @staticmethod
    def get_anim_from_file(filepath):
        if not os.path.exists(filepath):
            LOGGER.error("File not found: {}".format(filepath))
            return 

        with open(json_file, "r") as file_read:
            anim_curves = json.load(file_read)
        return anim_curves

class Pose(AnimBlock):
    def __init__(self, anim_curves=None):
        super(Pose, self).__init__(anim_curves)

    @property
    def frame():
        pass