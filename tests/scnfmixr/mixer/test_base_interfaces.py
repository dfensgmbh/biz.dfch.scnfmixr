# Copyright (c) 2024, 2025 d-fens GmbH, http://d-fens.ch
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Tests for signal_point2."""

import unittest

import biz.dfch.scnfmixr.public.mixer as pt


class AnAcquirableMixin(pt.IAcquirable):
    """AnAcquirable"""

    def acquire(self):
        """acquire"""
        raise NotImplementedError

    def release(self):
        """release"""
        raise NotImplementedError


class AConnectablePoint(AnAcquirableMixin, pt.IConnectablePoint):
    """MyConnectablePoint"""

    def __init__(self):
        super().__init__(str(id(self)))

    @property
    def is_source(self):
        raise NotImplementedError

    @property
    def is_sink(self):
        raise NotImplementedError

    @property
    def is_active(self):
        raise NotImplementedError

    def connect_to(self, other):
        raise NotImplementedError


class AConnectableSet(AnAcquirableMixin, pt.IConnectableSet):
    """MyConnectableSet"""

    def __init__(self):
        super().__init__(str(id(self)))

    @property
    def points(self):
        raise NotImplementedError

    def connect_to(self, other):
        raise NotImplementedError

    @property
    def is_source(self):
        raise NotImplementedError

    @property
    def is_sink(self):
        raise NotImplementedError


class AConnectableSource(AnAcquirableMixin, pt.IConnectableSource):
    """AConnectableSource"""

    def __init__(self):
        super().__init__(str(id(self)))

    @property
    def is_point(self):
        raise NotImplementedError

    @property
    def is_set(self):
        raise NotImplementedError

    def connect_to(self, other):
        raise NotImplementedError

    @property
    def is_sink(self):
        return False


class AConnectableSink(AnAcquirableMixin, pt.IConnectableSink):
    """AConnectableSource"""

    def __init__(self):
        super().__init__(str(id(self)))

    @property
    def is_point(self):
        raise NotImplementedError

    @property
    def is_set(self):
        raise NotImplementedError

    def connect_to(self, other):
        raise NotImplementedError

    @property
    def is_source(self):
        return False


class AConnectableSourcePoint(AnAcquirableMixin, pt.IConnectableSourcePoint):
    """AConnectableSourcePoint"""

    def __init__(self):
        super().__init__(str(id(self)))

    @property
    def is_active(self):
        raise NotImplementedError

    def connect_to(self, other):
        raise NotImplementedError

    @property
    def is_sink(self):
        return False


class AConnectableSinkPoint(AnAcquirableMixin, pt.IConnectableSinkPoint):
    """AConnectableSinkPoint"""

    def __init__(self):
        super().__init__(str(id(self)))

    @property
    def is_active(self):
        raise NotImplementedError

    def connect_to(self, other):
        raise NotImplementedError

    @property
    def is_source(self):
        return False


class AConnectableSourceSet(AnAcquirableMixin, pt.IConnectableSourceSet):
    """AConnectableSourceSet"""

    def __init__(self):
        super().__init__(str(id(self)))

    @property
    def points(self):
        raise NotImplementedError

    def connect_to(self, other):
        raise NotImplementedError

    @property
    def is_sink(self):
        return False


class AConnectableSinkSet(AnAcquirableMixin, pt.IConnectableSinkSet):
    """AConnectableSinkSet"""

    def __init__(self):
        super().__init__(str(id(self)))

    @property
    def points(self):
        raise NotImplementedError

    def connect_to(self, other):
        raise NotImplementedError

    @property
    def is_source(self):
        return False


class TestConnectablePoint(unittest.TestCase):
    """TestConnectablePoint."""

    def test_connectable_is_point_not_set(self):
        """test"""

        sut = AConnectablePoint()

        self.assertTrue(sut.is_point)
        self.assertFalse(sut.is_set)


class TestConnectableSet(unittest.TestCase):
    """TestConnectableSet."""

    def test_connectable_is_set_not_point(self):
        """test"""

        sut = AConnectableSet()

        self.assertFalse(sut.is_point)
        self.assertTrue(sut.is_set)


class TestConnectableSource(unittest.TestCase):
    """TestConnectableSource."""

    def test_connectable_is_source_not_sink(self):
        """test"""

        sut = AConnectableSource()

        self.assertTrue(sut.is_source)
        self.assertFalse(sut.is_sink)


class TestConnectableSink(unittest.TestCase):
    """TestConnectableSink."""

    def test_connectable_is_sink_not_source(self):
        """test"""

        sut = AConnectableSink()

        self.assertFalse(sut.is_source)
        self.assertTrue(sut.is_sink)


class TestConnectableSourcePoint(unittest.TestCase):
    """TestConnectableSourcePoint"""

    def test_connectable_is_source_point(self):
        """test"""

        sut = AConnectableSourcePoint()

        self.assertTrue(sut.is_source)
        self.assertFalse(sut.is_sink)
        self.assertTrue(sut.is_point)
        self.assertFalse(sut.is_set)


class TestConnectableSinkPoint(unittest.TestCase):
    """TestConnectableSinkPoint"""

    def test_connectable_is_sink_point(self):
        """test"""

        sut = AConnectableSinkPoint()

        self.assertFalse(sut.is_source)
        self.assertTrue(sut.is_sink)
        self.assertTrue(sut.is_point)
        self.assertFalse(sut.is_set)


class TestConnectableSourceSet(unittest.TestCase):
    """TestConnectableSourceSet"""

    def test_connectable_is_source_set(self):
        """test"""

        sut = AConnectableSourceSet()

        self.assertTrue(sut.is_source)
        self.assertFalse(sut.is_sink)
        self.assertFalse(sut.is_point)
        self.assertTrue(sut.is_set)


class TestConnectableSinkSet(unittest.TestCase):
    """TestConnectableSinkSet"""

    def test_connectable_is_sink_set(self):
        """test"""

        sut = AConnectableSinkSet()

        self.assertFalse(sut.is_source)
        self.assertTrue(sut.is_sink)
        self.assertFalse(sut.is_point)
        self.assertTrue(sut.is_set)
