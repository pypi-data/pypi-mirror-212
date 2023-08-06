# copyright ############################### #
# This file is part of the Xtrack Package.  #
# Copyright (c) CERN, 2021.                 #
# ######################################### #

from typing import Tuple
import numpy as np

import xobjects as xo
from .general import _print

from xobjects.struct import Struct, MetaStruct

from .line import Line, mk_class_namespace


class SerializationHeader(xo.Struct):
    """
    In a predetermined place in the buffer we have the metadata
    offset and the element type names. These have to be separate,
    because in order to rebuild TrackerData we need to first build
    ElementRefClass.
    """
    element_ref_data_offset = xo.UInt64
    reftype_names = xo.String[:]


class TrackerData:
    @staticmethod
    def generate_element_ref_data(element_ref_class) -> 'ElementRefData':
        class ElementRefData(Struct):
            elements = element_ref_class[:]
            names = xo.String[:]
            _overridable = False

        return ElementRefData

    def __init__(
            self,
            element_dict,
            element_names,
            element_s_locations,
            line_length,
            element_classes=None,
            extra_element_classes=(),
            element_ref_data=None,
            _context=None,
            _buffer=None,
            _offset=None,
    ):
        """
        Create an immutable line suitable for serialisation.

        Parameters
        ----------
        element_dict : dict
            Dictionary of elements, keyed by name.
        element_names : list
            List of element names.
        element_s_locations : list
            List of element s locations.
        line_length : float
            Length of the line.
        element_classes : list, optional
            Explicit list of classes of elements of the line; if `None`,
            will be inferred from list.
        extra_element_classes : tuple, optional
            If `element_classes` is `None`, this list will be used to augment
            the inferred list of element classes.
        element_ref_data : ElementRefData, optional
        """

        self._element_dict = element_dict
        self._element_names = tuple(element_names)
        self._elements = tuple([element_dict[ee] for ee in element_names])
        self._is_backtrackable = np.all([ee.has_backtrack for ee in self._elements])

        if _buffer is None:
            common_buffer = self.common_buffer_for_elements()
            if common_buffer is not None and _context in [common_buffer.context, None]:
                _buffer = common_buffer
            _buffer = _buffer or xo.get_a_buffer(context=_context, size=64)

        if not element_classes:
            element_classes = set(ee._XoStruct for ee in self._elements)
            element_classes |= set(extra_element_classes)
            element_classes = sorted(element_classes, key=lambda cc: cc.__name__)
        self.element_classes = element_classes

        class ElementRefClass(xo.UnionRef):
            _reftypes = self.element_classes

        self.element_s_locations = tuple(element_s_locations)
        self.line_length = line_length
        self._ElementRefClass = ElementRefClass
        if element_ref_data and element_ref_data._buffer is _buffer:
            self._element_ref_data = element_ref_data
        else:
            self._element_ref_data = self.move_elements_and_build_ref_data(_buffer)

    def common_buffer_for_elements(self):
        """If all `self.elements` elements are in the same buffer,
        returns said buffer, otherwise returns `None`."""
        common_buffer = None
        for ee in self._elements:
            if hasattr(ee, '_buffer'):
                if common_buffer is None:
                    common_buffer = ee._buffer

                if ee._buffer is not common_buffer:
                    return None

        return common_buffer

    def to_binary(self, buffer=None) -> Tuple[xo.context.XBuffer, int]:
        """
        Return a buffer containing a binary representation of the LineFrozen,
        together with the offset to the header in the buffer.
        These two are sufficient for recreating the line.
        """
        _element_ref_data = self._element_ref_data
        if not buffer:
            buffer = _element_ref_data._buffer

        if buffer is not _element_ref_data._buffer:
            _element_ref_data = self.move_elements_and_build_ref_data(buffer)

        header = self.build_header(
            buffer=buffer,
            element_ref_data_offset=_element_ref_data._offset,
        )

        return buffer, header._offset

    def build_header(self, buffer, element_ref_data_offset) -> SerializationHeader:
        """
        Build a serialization header in the buffer. This contains all
        the necessary for decoding the line metadata.
        """
        return SerializationHeader(
            element_ref_data_offset=element_ref_data_offset,
            reftype_names=[
                reftype._DressingClass.__name__
                for reftype in self._ElementRefClass._reftypes
            ],
            _buffer=buffer,
        )

    def move_elements_and_build_ref_data(self, buffer):
        """
        Ensure all the elements of the line are in the buffer (which will be
        created if `buffer` is equal to `None`), and write the line metadata
        to it. If the buffer is empty, the metadata will be at the beginning.
        Returns the metadata xobject.
        """
        element_refs_cls = self.generate_element_ref_data(self._ElementRefClass)

        element_ref_data = element_refs_cls(
            elements=len(self._elements),
            names=list(self._element_names),
            _buffer=buffer,
        )

        # Move all the elements into buffer, so they don't get duplicated.
        # We only do it now, as we need to make sure element_ref_data is already
        # allocated after reftype_names.
        moved_element_dict = {}
        for name, elem in self._element_dict.items():
            if elem._buffer is not buffer:
                elem.move(_buffer=buffer)
            moved_element_dict[name] = elem._xobject

        element_ref_data.elements = [
            moved_element_dict[name] for name in self.element_names
        ]

        return element_ref_data

    @classmethod
    def from_binary(
        cls,
        buffer: xo.context.XBuffer,
        header_offset: int,
        extra_element_classes: tuple = (),
    ) -> 'TrackerData':
        header = SerializationHeader._from_buffer(
            buffer=buffer,
            offset=header_offset,
        )

        element_hybrid_classes = []
        element_namespace = mk_class_namespace(extra_classes=extra_element_classes)
        for reftype in header.reftype_names:
            if hasattr(element_namespace, reftype):
                element_hybrid_classes.append(getattr(element_namespace, reftype))
            else:
                ValueError(f'Cannot find the type `{reftype}`. Is it custom '
                           f'and you forgot to include the class in '
                           f'`extra_element_classes`?')

        # With the reftypes loaded we can create our classes
        element_classes = [elem._XoStruct for elem in element_hybrid_classes]

        class ElementRefClass(xo.UnionRef):
            _reftypes = element_classes

        # We can now load the line from the buffer
        element_refs_cls = cls.generate_element_ref_data(ElementRefClass)
        element_ref_data = element_refs_cls._from_buffer(
            buffer=buffer,
            offset=int(header.element_ref_data_offset)
        )

        # Recreate and redress line elements
        hybrid_cls_for_xstruct = {
            elem._XoStruct: elem for elem in element_hybrid_classes
        }

        element_dict = {}
        num_elements = len(element_ref_data.elements)
        elements = element_ref_data.elements
        names = element_ref_data.names
        for ii, elem in enumerate(elements):
            _print('Loading line from binary: '
                f'{round(ii/num_elements*100):2d}%  ',end="\r", flush=True)
            name = names[ii]
            if name in element_dict:
                continue

            hybrid_cls = hybrid_cls_for_xstruct[elem.__class__]
            element_dict[name] = hybrid_cls(_xobject=elem)

        temp_line = Line(
            elements=element_dict,
            element_names=element_ref_data.names,
        )
        tracker_data = TrackerData(
            element_dict=temp_line.element_dict,
            element_names=temp_line.element_names,
            element_s_locations=temp_line.get_s_elements(),
            line_length=temp_line.get_length(),
            element_classes=element_classes,
            element_ref_data=element_ref_data,
        )
        tracker_data._ElementRefClass = ElementRefClass

        return tracker_data

    @property
    def elements(self):
        return self._elements

    @property
    def element_names(self):
        return self._element_names

    @property
    def _buffer(self):
        return self._element_ref_data._buffer

    @property
    def _offset(self):
        return self._element_ref_data._offset

    @property
    def _context(self):
        return self._element_ref_data._context

    def __getstate__(self):
        out = self.__dict__.copy()
        out['_element_ref_data'] = (
            self._element_ref_data._buffer, self._element_ref_data._offset)
        out['_ElementRefClass'] = None
        out['element_classes'] = [cc._DressingClass for cc in self.element_classes]
        return out

    def __setstate__(self, state):
        buffer, offset = state.pop('_element_ref_data')
        self.__dict__.update(state)
        self.element_classes = [cc._XoStruct for cc in self.element_classes]

        class ElementRefClass(xo.UnionRef):
            _reftypes = self.element_classes

        self._ElementRefClass = ElementRefClass
        element_refs_cls = self.generate_element_ref_data(self._ElementRefClass)
        self._element_ref_data = element_refs_cls._from_buffer(
            buffer=buffer,
            offset=offset,
        )

