# MIT License

# Copyright (c) 2025 d-fens GmbH, http://d-fens.ch

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Module path_creator."""

from typing import cast

from biz.dfch.logging import log

from biz.dfch.scnfmixr.public.mixer import (
    ISignalPath,
    IConnectableSink,
    IConnectableSinkPoint,
    IConnectableSinkSet,
    IConnectableSource,
    IConnectableSourcePoint,
    IConnectableSourceSet,
    State,
    ConnectionPolicy,
    ConnectionPolicyException,
)
from .jack_signal_path import JackSignalPath


class PathCreator:
    """PathCreator

    * Each `process_` method will return a list of tuples representing the
    created signal paths.
    * The returned items will either be new ISignalPath instances,
    instances from `paths.values()` or a combination thereof.
    * If a new signal path is created, the value `PathState` will be set to
    `PathStateFlag.INITIAL`. 
    * The returned items will **not** have been added to `paths`. The caller
    has to do this, if she so chooses.
    * If `paths` is a shared resource, the caller has to ensure locking its
    access.
    * If the result list is empty, no possible connections could satisfy the
    connection policy request, eg. the source or sink set is empty.
    * The result will never be None.
    * The `key` of `paths` *dict* is expected to be `ISignalPath.name`.

    Returns:
        list (tuple[PathState, ISignalPath]): The list of signal paths,
        satisfying the ConnectionPolicy request.

    Raises:
        ValueError: Raised, when the combination of source and sink is
            incompatible with the ConnectionPolicy request.
    """

    _COUNT_MONO = 1
    _COUNT_DUAL = 2
    _IDX_MONO = 0
    _IDX_LEFT = _IDX_MONO
    _IDX_RIGHT = 1

    _items: dict[str, tuple[State, ISignalPath]]

    def __init__(self,
                 items: dict[str,
                             tuple[State, ISignalPath]]
                 ) -> None:
        """
        Args:
            items (dict[str, tuple[PathState, ISignalPath]]): A map consisting
                of signal paths and its state. The key is `ISignalPath.name`.

                **Note**: The access to this parameter is **not** synchronised.
        """

        assert isinstance(items, dict)

        self._items = items

    def _get_single_path(
            self,
            source: IConnectableSourcePoint,
            sink: IConnectableSinkPoint
    ) -> tuple[State, ISignalPath]:

        assert isinstance(source, IConnectableSource), source.name
        assert isinstance(sink, IConnectableSink), sink.name

        result: tuple[State, ISignalPath]

        state = State()
        path = JackSignalPath(source, sink, state)
        key = path.name

        if key in self._items:
            result = self._items[key]
        else:
            result = (state, path)

        return result

    def process_mono(
            self,
            source: IConnectableSource,
            sink: IConnectableSink,
    ) -> list[tuple[State, ISignalPath]]:
        """ConnectionPolicy.MONO"""

        assert isinstance(source, IConnectableSource)
        assert isinstance(sink, IConnectableSink)

        if source.is_point and sink.is_point:
            source_point = source
            sink_point = sink

            return [self._get_single_path(source_point, sink_point)]

        if source.is_point and sink.is_set:
            source_point = cast(IConnectableSourcePoint, source)

            sink_set = cast(IConnectableSinkSet, sink)
            if self._COUNT_MONO > len(sink_set.points):
                raise ConnectionPolicyException(
                    ConnectionPolicy.MONO,
                    source,
                    sink
                )
            sink_point = cast(IConnectableSinkPoint,
                              sink_set.points[self._IDX_MONO])

            return [self._get_single_path(source_point, sink_point)]

        if source.is_set and sink.is_point:
            source_set = cast(IConnectableSourceSet, source)
            if self._COUNT_MONO > len(source_set.points):
                raise ConnectionPolicyException(
                    ConnectionPolicy.MONO,
                    source,
                    sink
                )
            source_point = cast(IConnectableSourcePoint,
                                source_set[self._IDX_MONO])

            sink_point = cast(IConnectableSinkPoint, sink)

            return [self._get_single_path(source_point, sink_point)]

        if source.is_set and sink.is_set:
            source_set = cast(IConnectableSourceSet, source)
            if self._COUNT_MONO > len(source_set.points):
                raise ConnectionPolicyException(
                    ConnectionPolicy.MONO,
                    source,
                    sink
                )
            source_point = cast(IConnectableSourcePoint,
                                source_set[self._IDX_MONO])

            sink_set = cast(IConnectableSinkSet, sink)
            if self._COUNT_MONO > len(sink_set.points):
                raise ConnectionPolicyException(
                    ConnectionPolicy.MONO,
                    source,
                    sink
                )
            sink_point = cast(IConnectableSinkPoint,
                              sink_set.points[self._IDX_MONO])

            return [self._get_single_path(source_point, sink_point)]

        raise ConnectionPolicyException(
            ConnectionPolicy.MONO,
            source,
            sink
        )

    def process_dual(
            self,
            source: IConnectableSource,
            sink: IConnectableSink,
    ) -> list[tuple[State, ISignalPath]]:
        """ConnectionPolicy.DUAL"""

        assert isinstance(source, IConnectableSource)
        assert isinstance(sink, IConnectableSink)

        log.debug("process_dual: source '%s' [%s]; sink '%s' [%s]",
                  source.name,
                  type(source),
                  sink.name,
                  type(sink))

        if not isinstance(source, IConnectableSourceSet):
            raise ConnectionPolicyException(
                ConnectionPolicy.DUAL,
                source,
                sink
            )
        if not isinstance(sink, IConnectableSinkSet):
            raise ConnectionPolicyException(
                ConnectionPolicy.DUAL,
                source,
                sink
            )

        if source.is_point and sink.is_set:
            source_point_l = cast(IConnectableSourcePoint, source)

            sink_set = cast(IConnectableSinkSet, sink)
            if self._COUNT_DUAL > len(sink_set.points):
                raise ConnectionPolicyException(
                    ConnectionPolicy.DUAL,
                    source,
                    sink
                )
            sink_point_l = cast(IConnectableSinkPoint,
                                sink_set.points[self._IDX_LEFT])
            sink_point_r = cast(IConnectableSinkPoint,
                                sink_set.points[self._IDX_RIGHT])

            return [
                self._get_single_path(source_point_l, sink_point_l),
                self._get_single_path(source_point_l, sink_point_r)
            ]

        if source.is_set and sink.is_set:
            source_set = cast(IConnectableSourceSet, source)
            if self._COUNT_MONO == len(source_set.points):
                source_point_l = cast(IConnectableSourcePoint,
                                      source_set[self._IDX_LEFT])
                source_point_r = cast(IConnectableSourcePoint,
                                      source_set[self._IDX_LEFT])
            else:
                if self._COUNT_DUAL > len(source_set.points):
                    raise ConnectionPolicyException(
                        ConnectionPolicy.DUAL,
                        source,
                        sink
                    )
                source_point_l = cast(IConnectableSourcePoint,
                                      source_set[self._IDX_LEFT])
                source_point_r = cast(IConnectableSourcePoint,
                                      source_set[self._IDX_RIGHT])

            sink_set = cast(IConnectableSinkSet, sink)
            if self._COUNT_DUAL > len(sink_set.points):
                raise ConnectionPolicyException(
                    ConnectionPolicy.DUAL,
                    source,
                    sink
                )
            sink_point_l = cast(IConnectableSinkPoint,
                                sink_set.points[self._IDX_LEFT])
            sink_point_r = cast(IConnectableSinkPoint,
                                sink_set.points[self._IDX_RIGHT])

            return [
                self._get_single_path(source_point_l, sink_point_l),
                self._get_single_path(source_point_r, sink_point_r)
            ]

        raise ConnectionPolicyException(
            ConnectionPolicy.DUAL,
            source,
            sink
        )

    def process_line(
            self,
            source: IConnectableSource,
            sink: IConnectableSink,
    ) -> list[tuple[State, ISignalPath]]:
        """ConnectionPolicy.LINE"""

        assert isinstance(source, IConnectableSource)
        assert isinstance(sink, IConnectableSink)

        if source.is_point and sink.is_point:
            source_point = source
            sink_point = sink

            return [self._get_single_path(source_point, sink_point)]

        if source.is_point and sink.is_set:
            source_point = cast(IConnectableSourcePoint, source)

            sink_set = cast(IConnectableSinkSet, sink)
            sink_point = cast(IConnectableSinkPoint,
                              sink_set.points[self._IDX_MONO])

            if self._COUNT_MONO != len(sink_set.points):
                raise ConnectionPolicyException(
                    ConnectionPolicy.LINE,
                    source,
                    sink
                )

            return [self._get_single_path(source_point, sink_point)]

        if source.is_set and sink.is_point:
            source_set = cast(IConnectableSourceSet, source)
            if self._COUNT_MONO != len(source_set.points):
                raise ConnectionPolicyException(
                    ConnectionPolicy.LINE,
                    source,
                    sink
                )
            source_point = cast(IConnectableSourcePoint,
                                source_set[self._IDX_MONO])
            sink_point = cast(IConnectableSinkPoint, sink)

            return [self._get_single_path(source_point, sink_point)]

        if source.is_set and sink.is_set:
            source_set = cast(IConnectableSourceSet, source)
            if self._COUNT_MONO > len(source_set.points):
                raise ConnectionPolicyException(
                    ConnectionPolicy.LINE,
                    source,
                    sink
                )

            sink_set = cast(IConnectableSinkSet, sink)
            if self._COUNT_MONO > len(sink_set.points):
                raise ConnectionPolicyException(
                    ConnectionPolicy.LINE,
                    source,
                    sink
                )

            if len(source_set.points) != len(sink_set.points):
                raise ConnectionPolicyException(
                    ConnectionPolicy.LINE,
                    source,
                    sink
                )

            count = len(source_set.points)
            result: list[tuple[State, ISignalPath]] = []
            for i in range(count):
                source_point = source_set.points[i]
                sink_point = sink_set.points[i]
                result.append(self._get_single_path(source_point, sink_point))

            return result

        raise ConnectionPolicyException(
            ConnectionPolicy.LINE,
            source,
            sink
        )

    def process_bcast(
            self,
            source: IConnectableSource,
            sink: IConnectableSink,
    ) -> list[tuple[State, ISignalPath]]:
        """ConnectionPolicy.BCAST"""

        assert isinstance(source, IConnectableSource)
        assert isinstance(sink, IConnectableSink)

        if source.is_set:
            raise ConnectionPolicyException(
                ConnectionPolicy.BCAST,
                source,
                sink
            )

        source_point = source

        if sink.is_point:
            sink_point = sink

            return [self._get_single_path(source_point, sink_point)]

        sink_set = cast(IConnectableSinkSet, sink)
        if self._COUNT_MONO > len(sink_set.points):
            raise ConnectionPolicyException(
                ConnectionPolicy.BCAST,
                source,
                sink
            )

        result: list[tuple[State, ISignalPath]] = []
        for sink_point in sink_set.points:
            result.append(self._get_single_path(source_point, sink_point))

        return result

    def process_merge(
            self,
            source: IConnectableSource,
            sink: IConnectableSink,
    ) -> list[tuple[State, ISignalPath]]:
        """ConnectionPolicy.MERGE"""

        assert isinstance(source, IConnectableSource)
        assert isinstance(sink, IConnectableSink)

        if sink.is_set:
            sink_set = cast(IConnectableSinkSet, sink)
            if self._COUNT_MONO > len(sink_set.points):
                raise ConnectionPolicyException(
                    ConnectionPolicy.MERGE,
                    source,
                    sink
                )
            sink_point = sink_set[self._IDX_MONO]
        else:
            sink_point = sink

        if source.is_point:
            source_point = source

            return [self._get_single_path(source_point, sink_point)]

        source_set = cast(IConnectableSourceSet, source)
        if self._COUNT_MONO > len(source_set.points):
            raise ConnectionPolicyException(
                ConnectionPolicy.MERGE,
                source,
                sink
            )

        result: list[tuple[State, ISignalPath]] = []
        for source_point in source_set:
            result.append(self._get_single_path(source_point, sink_point))

        return result

    def process_trunc(
            self,
            source: IConnectableSource,
            sink: IConnectableSink,
    ) -> list[tuple[State, ISignalPath]]:
        """ConnectionPolicy.TRUNC"""

        assert isinstance(source, IConnectableSource)
        assert isinstance(sink, IConnectableSink)

        if source.is_point and sink.is_point:
            source_point = source
            sink_point = sink

            return [self._get_single_path(source_point, sink_point)]

        if source.is_point and sink.is_set:
            source_point = cast(IConnectableSourcePoint, source)
            sink_set = cast(IConnectableSinkSet, sink)
            sink_point = cast(IConnectableSinkPoint,
                              sink_set.points[self._IDX_MONO])

            if self._COUNT_MONO != len(sink_set.points):
                raise ConnectionPolicyException(
                    ConnectionPolicy.TRUNC,
                    source,
                    sink
                )

            return [self._get_single_path(source_point, sink_point)]

        if source.is_set and sink.is_point:
            source_set = cast(IConnectableSourceSet, source)
            if self._COUNT_MONO != len(source_set.points):
                raise ConnectionPolicyException(
                    ConnectionPolicy.TRUNC,
                    source,
                    sink
                )
            source_point = cast(IConnectableSourcePoint,
                                source_set[self._IDX_MONO])
            sink_point = cast(IConnectableSinkPoint, sink)

            return [self._get_single_path(source_point, sink_point)]

        if source.is_set and sink.is_set:
            source_set = cast(IConnectableSourceSet, source)
            if self._COUNT_MONO > len(source_set.points):
                raise ConnectionPolicyException(
                    ConnectionPolicy.TRUNC,
                    source,
                    sink
                )

            sink_set = cast(IConnectableSinkSet, sink)
            if self._COUNT_MONO > len(sink_set.points):
                raise ConnectionPolicyException(
                    ConnectionPolicy.TRUNC,
                    source,
                    sink
                )

            if len(source_set.points) != len(sink_set.points):
                raise ConnectionPolicyException(
                    ConnectionPolicy.TRUNC,
                    source,
                    sink
                )

            count = min(len(source_set.points), len(sink_set.points))
            result: list[tuple[State, ISignalPath]] = []
            for i in range(count):
                source_point = source_set.points[i]
                sink_point = sink_set.points[i]
                result.append(self._get_single_path(source_point, sink_point))

            return result

        raise ConnectionPolicyException(
            ConnectionPolicy.TRUNC,
            source,
            sink
        )

    def process_default(
            self,
            source: IConnectableSource,
            sink: IConnectableSink,
    ) -> list[tuple[State, ISignalPath]]:
        """ConnectionPolicy.DEFAULT"""

        assert isinstance(source, IConnectableSource)
        assert isinstance(sink, IConnectableSink)

        return self.process_dual(source, sink)
