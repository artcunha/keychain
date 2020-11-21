import maya.mel
import maya.cmds as cmds
import maya.api.OpenMaya as om
import maya.api.OpenMayaAnim as omAnim

class Timeline(object):
    def __init__(self):
        pass

    def loop_through(self, frame_range=None, full_range=False):
        frame_range = frame_range or (self.anim_frame_range if full_range else self.frame_range)
        for frame in xrange(*frame_range):
            yield frame


    def scrub_timeline(self, frameRange=None, full_range=False):
        current_time = self.current_time
        frame_range = frame_range or (self.anim_frame_range if full_range else self.frame_range)
        for frame in xrange(*frameRange):
            yield frame
            omAnim.MAnimControl.setCurrentTime(self._frame_to_time(frame))

        omAnim.MAnimControl.setCurrentTime(current_time)


    @staticmethod
    def get_stepped_frames(frame_range, step=1, full_range=False):
        frame_range = frame_range or (self.anim_frame_range if full_range else self.frame_range)
        start, end = frame_range
        frames = []
        while start < end:
            frames.append(start)
            start += step
        return frames


    @property
    def anim_frame_range(self):
        return (self.start_frame, self.end_frame)

    @property
    def frame_range(self):
        return (self.min_frame, self.max_frame)

    @property
    def time_range(self):
        return (self.min_time, self.max_time)

    @staticmethod
    def get_timeslider_range():
        aTimeSlider = maya.mel.eval("$tmpVar=$gPlayBackSlider")
        return cmds.timeControl(aTimeSlider, q=True, rangeArray=True)

    def get_selected_range(self):
        return Timeline.get_timeslider_range() or self.frame_range
    

    def _frame_to_time(self, frame):
        return om.MTime(frame, om.MTime.kFilm)

    def _time_to_frame(self, time):
        return int(time.asUnits(om.MTime.kFilm))

    ######## FRAMES
    @property
    def current_frame(self):
        return self._time_to_frame(self.current_time)

    @current_frame.setter
    def current_frame(self, frame):
        return omAnim.MAnimControl.setCurrentTime(self._frame_to_time(frame))

    @property
    def min_frame(self):
        return self._time_to_frame(self.min_time)

    @min_frame.setter
    def min_frame(self, frame):
        return omAnim.MAnimControl.setMinTime(self._frame_to_time(frame))

    @property
    def max_frame(self):
        return self._time_to_frame(self.max_time)

    @max_frame.setter
    def max_frame(self, frame):
        return omAnim.MAnimControl.setMaxTime(self._frame_to_time(frame))

    @property
    def start_frame(self):
        return self._time_to_frame(self.start_time)

    @start_frame.setter
    def start_frame(self, frame):
        return omAnim.MAnimControl.setAnimationStartTime(self._frame_to_time(frame))

    @property
    def end_frame(self):
        return self._time_to_frame(self.end_frame)

    @end_frame.setter
    def end_frame(self, frame):
        return omAnim.MAnimControl.setAnimationEndTime(self._frame_to_time(frame))

    ######## TIME
    @property
    def current_time(self):
        return omAnim.MAnimControl.currentTime()

    @current_time.setter
    def current_time(self, time):
        return omAnim.MAnimControl.setCurrentTime(time)

    @property
    def min_time(self):
        return omAnim.MAnimControl.minTime()

    @min_time.setter
    def min_time(self, time):
        return omAnim.MAnimControl.setMinTime(time)

    @property
    def max_time(self):
        return omAnim.MAnimControl.maxTime()

    @max_time.setter
    def max_time(self, time):
        return omAnim.MAnimControl.setMaxTime(time)

    @property
    def start_time(self):
        return omAnim.MAnimControl.animationStartTime()

    @start_time.setter
    def start_time(self, time):
        return omAnim.MAnimControl.setAnimationStartTime(time)

    @property
    def end_time(self):
        return omAnim.MAnimControl.animationEndTime()

    @end_time.setter
    def end_time(self, time):
        return omAnim.MAnimControl.setAnimationEndTime(time)
