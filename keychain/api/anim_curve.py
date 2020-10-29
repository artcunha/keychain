# -*- coding: utf-8 -*-
"""
Animation data utilities.

This module aims to provide friendly interface for getting and transfering animation data.

Example:
    Assuming a source dependency node has been animated. Selecting source first, target last:
    from maya import cmds
    source, target = cmds.ls(sl=True, l=True)
    anim_data = get_node_anim_data(source) #collect the data
    set_node_anim_data(target, anim_data) #set the data

Todo:
    Extend documentation. Add support for containers.

.. moduleauthor:: Christian López Barrón <christianlb.vfx@outlook.com>

"""

# standard
import re
import sys
import logging
import traceback
import maya.api.OpenMaya as om2
import maya.api.OpenMayaAnim as omanim

from keychain.api.utils import strings
from keychain.api.utils import openMaya as maya_api_utils

LOGGER = logging.getLogger(__name__)


_API_SOURCE = {'curve': {'isStatic', 'isWeighted', 'preInfinityType', 'postInfinityType'},
               'key': {'value', 'isBreakdown', 'tangentsLocked', 'inTangentType', 'outTangentType'}}

_API_ATTRS = {level: {strings.toUnderscores(attr): attr for attr in _API_SOURCE[level]} for level in _API_SOURCE}


_RE_OBJ_EXT = re.compile('(Object does not exist)')


class AnimCurve(object):
    @classmethod
    def from_mcurve(mcurve):
        pass


    @classmethod
    def from_node(cls, dg_name):
        anim_data = cls.get_node_anim_data(dg_name)
        return cls(anim_data)


    def __init__(self, data):
        self.data = data


    @staticmethod
    def get_node_anim_data(dg_name):
        """
        Get the animation data for a specific node.
        All of its animCurves connections are searched and processed.

        Args:
            dg_name (str): Node to get the animation data from2.

        Returns:
            dict: The collected animation data. See also getAnimCurvesData
        """
        return {data['destination']['attr']: data for data in it_node_anim_curves_data(dg_name,
                                                                                        get_node_anim_curves(dg_name))}

    @staticmethod
    def set_node_anim_data(dg_name, data):
        """
        Set animation data to a specific dependency node.

        Args:
            dg_name (str): Node to set the animation data to.
            data (dict): Data to set to the curve node. see getAnimCurveData
        """
        omslist = om2.MSelectionList()
        for i, (attr, curve_data) in enumerate(data.iteritems()):
            plug_path = '{}.{}'.format(dg_name, attr)
            try:
                omslist.add(plug_path)
            except RuntimeError:
                tback = traceback.format_exc()
                if _RE_OBJ_EXT.search(tback):
                    msg = 'Could not set data on "{}" as it does not exist'.format(plug_path, traceback.format_exc())
                    LOGGER.error(msg)
                    continue
                else:
                    LOGGER.critical(tback)
                    raise
            _set_attribute_anim_data(omslist.getPlug(i), curve_data['data'])

    def _anim_curve_data(mcurve):
        data = {at_k:getattr(mcurve, at_api) for at_k, at_api in _API_ATTRS['curve'].iteritems()}
        data['keys'] = {k_i : _anim_curve_key_data(mcurve, k_i) for k_i in xrange(mcurve.numKeys)}
        return data


    def _anim_curve_key_data(mcurve, index):
        data = {at_k:getattr(mcurve, at_api)(index) for at_k, at_api in _API_ATTRS['key'].iteritems()}
        data.update(time=mcurve.input(index).value,
                    in_tangent={'xy' : mcurve.getTangentXY(index, True)},
                    out_tangent={'xy' : mcurve.getTangentXY(index, False)})
        return data


    def get_anim_curve_data(mcurve, target_dg_name=None):
        """
        Collect data from a specific animation curve node.

        Normally you do not need to call this function directly:
        getNodeAnimData and getAnimCurvesData provide a higher-level interface for getting animation data.

        Args:
            mcurve (maya.api.OpenMayaAnim.MFnAnimCurve): MObject to extract data from2.
            target_dg_name (Optional[str]): Traverse the graph to know the attribute being affected by the curve
                                            on a specified targe dependency node.
        Returns:
            dict: The collected data in form of a dictionary.
        """
        outputs = mcurve.findPlug('output', False).destinations()
        if target_dg_name:
            output = maya_api_utils.find_plug(target_dg_name, outputs)
            if not output:
                msg = 'No connection was found between "{}" and target node "{}".'.format(mcurve.name(), target_dg_name)
                raise exceptions.OutputError(msg)
        else:
            output = outputs[0]
        destination = {'node': maya_api_utils.get_mdependency_node_path(output.node())[1],
                       'attr': output.partialName(useLongNames=True)}
        data = _anim_curve_data(mcurve)
        return {'outputs': [o.partialName(includeNodeName=True,useLongNames=True) for o in outputs],
                'destination': destination, 'data': data}


    def it_anim_curves_data(*dg_names):
        """
        Gather data from the specified animation curve nodes.

        Args:
            *dg_names (str): Animation node dg names to process.

        Returns:
            dict: The collected data of each curve.
        """
        omslist = om2.MSelectionList()
        for i, c in enumerate(dg_names):
            omslist.add(c)
            mcurve = omanim.MFnAnimCurve(omslist.getDependNode(i))
            yield get_anim_curve_data(mcurve)


    def it_node_anim_curves_data(dg_name, mitsel):
        while not mitsel.isDone():
            mcurve = omanim.MFnAnimCurve(mitsel.getDependNode())
            try:
                curve_data = get_anim_curve_data(mcurve, dg_name)
            except exceptions.OutputError:
                msg = '{} Skipping curve data.'.format(sys.exc_info()[1])
                LOGGER.warning(msg)
            else:
                yield curve_data
            finally:
                mitsel.next()


    def get_node_anim_curves(dg_name):
        """
        Get the curves connected (directly or indirectly) to a dg node.
        It searches recusively until finding a transofm node or a constraint,
        taking pairBlend, mute, conversion nodes, etc as bridge nodes.

        Args:
            dg_name (str): Node to get its connected animation curves.

        Returns:
            set: Found animCurves with connections to the dg node.
        """
        omlist = om2.MSelectionList()
        omlist.add(dg_name)
        mobj = omlist.getDependNode(0)
        mdep = om2.MFnDependencyNode(mobj)
        found, __ = _get_node_anim_curves(mdep, om2.MSelectionList(), om2.MSelectionList())
        return om2.MItSelectionList(found)


    def _get_node_anim_curves(dg_node, found, searched):
        for c in dg_node.getConnections():
            source_plug = c.source()
            if source_plug.isNull or searched.hasItem(source_plug): # skip empty plugs
                continue
            searched.add(source_plug)
            source_node = source_plug.node()
            source_type = source_node.apiTypeStr
            # care only for curveTime nodes
            if source_type.startswith('kAnimCurveTime') and not found.hasItem(source_node):
                found.add(source_node)
            elif source_type.endswith('Constraint') or source_type == 'kTransform':
                continue
            else:
                found, searched = _get_node_anim_curves(om2.MFnDependencyNode(source_node), found, searched)
        return found, searched

    def _set_attribute_anim_data(mplug, data):
        mcurve = omanim.MFnAnimCurve(mplug)
        try:
            mcurve.name() #errors if does not exist
        except RuntimeError:
            mcurve.create(mplug) #create one if didn't exist
        set_anim_curve_data(mcurve, data)

    def set_anim_curve_data(mcurve, data):
        """
        Set animation data to a specific animation curve node.

        Normally you do not need to call this function directly:
        setNodeAnimData provides a higher-level interface for setting animation data.

        Args:
            mcurve (maya.api.OpenMayaAnim.MFnAnimCurve): MObject to extract data from2.
            data (dict): Data to set to the curve node. see getAnimCurveData
        """
        mcurve.setIsWeighted(data['is_weighted'])
        mcurve.setPreInfinityType(data['pre_infinity_type'])
        mcurve.setPostInfinityType(data['post_infinity_type'])
        for k_i, k_values in data['keys'].iteritems():
            k_time = om2.MTime(k_values['time'])
            if not mcurve.find(k_time):
                mcurve.addKey(k_time, k_values['value'])
            _set_anim_curve_key_data(mcurve, mcurve.find(k_time), k_values)

    def _set_anim_curve_key_data(mcurve, index, data):
        mcurve.setTangentsLocked(index, False)
        mcurve.setInTangentType(index, data['in_tangent_type'])
        x, y = data['in_tangent']['xy']
        mcurve.setTangent(index, x, y, True, convertUnits=False) #IN TANGENT
        mcurve.setOutTangentType(index, data['out_tangent_type'])
        x, y = data['out_tangent']['xy']
        mcurve.setTangent(index, x, y, False, convertUnits=False) #OUT TANGENT
        mcurve.setIsBreakdown(index, data['is_breakdown'])
        if data['tangents_locked']:
            mcurve.setTangentsLocked(index, True)

"""
Example of data:
{u'|pCube1': {u'translateX': {'data': {
    'is_static': False,
    'is_weighted': False,
    'keys': {0: {'in_tangent': {'xy': (1.0,
                                        0.0)},
                'in_tangent_type': 2,
                'is_breakdown': False,
                'out_tangent': {'xy': (0.2140544354915619,
                                        0.9768217206001282)},
                'out_tangent_type': 2,
                'tangents_locked': True,
                'time': 1.0,
                'value': -5.394801740406098},
            1: {'in_tangent': {'xy': (0.2140544354915619,
                                        0.9768217206001282)},
                'in_tangent_type': 2,
                'is_breakdown': False,
                'out_tangent': {'xy': (1.0,
                                        0.0)},
                'out_tangent_type': 2,
                'tangents_locked': True,
                'time': 60.0,
                'value': 5.8236216588255445}},
    'post_infinity_type': 4,
    'pre_infinity_type': 4},
    'destination': {'attr': u'translateX',
                'node': u'|pCube1'},
    'is_blended': False,
    'outputs': [u'pCube1.translateX']},
 u'|pSphere1': {u'translateX': {'data': {'is_static': False,
"""