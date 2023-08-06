# The purpose of this file is to provide Pythonic wrapper on top
# the native precompiled CPython module. It improves compatibility
# Python tooling, linters, and static analyzers. It also embeds JIT
# into the primary `Index` class, connecting USearch with Numba.
import os
from math import sqrt
from typing import Optional, Callable, Union, NamedTuple, List

import numpy as np

from usearch.compiled import Index as _CompiledIndex
from usearch.compiled import SetsIndex as _CompiledSetsIndex
from usearch.compiled import BitsIndex as _CompiledBitsIndex

from usearch.compiled import MetricKind
from usearch.compiled import (
    DEFAULT_CONNECTIVITY,
    DEFAULT_EXPANSION_ADD,
    DEFAULT_EXPANSION_SEARCH,
)

BitwiseMetricKind = (
    MetricKind.BitwiseHamming,
    MetricKind.BitwiseTanimoto,
    MetricKind.BitwiseSorensen,
)

SetsIndex = _CompiledSetsIndex


class Matches(NamedTuple):
    labels: np.ndarray
    distances: np.ndarray
    counts: np.ndarray


def list_matches(results: Matches, row: int) -> List[dict]:

    count = results[2][row]
    labels = results[0][row, :count]
    distances = results[1][row, :count]
    return [
        {'label': int(label), 'distance': float(distance)}
        for label, distance in zip(labels, distances)
    ]


def jit_metric(ndim: int, metric: MetricKind, dtype: str = 'f32') -> Callable:

    try:
        from numba import cfunc, types, carray
    except ImportError:
        raise ModuleNotFoundError(
            'To use JIT install Numba with `pip install numba`.'
            'Alternatively, reinstall usearch with `pip install usearch[jit]`')

    # Showcases how to use Numba to JIT-compile similarity measures for USearch.
    # https://numba.readthedocs.io/en/stable/reference/jit-compilation.html#c-callbacks

    if dtype == 'f32':
        signature = types.float32(
            types.CPointer(types.float32),
            types.CPointer(types.float32),
            types.uint64, types.uint64)

        if metric == MetricKind.IP:

            @cfunc(signature)
            def numba_ip(a, b, _n, _m):
                a_array = carray(a, ndim)
                b_array = carray(b, ndim)
                ab = 0.0
                for i in range(ndim):
                    ab += a_array[i] * b_array[i]
                return 1 - ab

            return numba_ip

        if metric == MetricKind.Cos:

            @cfunc(signature)
            def numba_cos(a, b, _n, _m):
                a_array = carray(a, ndim)
                b_array = carray(b, ndim)
                ab = 0.0
                a_sq = 0.0
                b_sq = 0.0
                for i in range(ndim):
                    ab += a_array[i] * b_array[i]
                    a_sq += a_array[i] * a_array[i]
                    b_sq += b_array[i] * b_array[i]
                a_norm = sqrt(a_sq)
                b_norm = sqrt(b_sq)
                if a_norm == 0 and b_norm == 0:
                    return 0
                elif a_norm == 0 or b_norm == 0 or ab == 0:
                    return 1
                else:
                    return 1 - ab / (a_norm * b_norm)

            return numba_cos

        if metric == MetricKind.L2sq:

            @cfunc(signature)
            def numba_l2sq(a, b, _n, _m):
                a_array = carray(a, ndim)
                b_array = carray(b, ndim)
                ab_delta_sq = types.float32(0.0)
                for i in range(ndim):
                    ab_delta_sq += (a_array[i] - b_array[i]) * \
                        (a_array[i] - b_array[i])
                return ab_delta_sq

            return numba_l2sq

    return None


class Index:
    """Fast JIT-compiled vector-search index for dense equi-dimensional embeddings.

    Vector labels must be integers.
    Vectors must have the same number of dimensions within the index.
    Supports Inner Product, Cosine Distance, Ln measures
    like the Euclidean metric, as well as automatic downcasting
    and quantization.
    """

    def __init__(
        self,
        ndim: int,
        metric: Union[MetricKind, Callable] = MetricKind.IP,
        dtype: Optional[str] = None,
        jit: bool = False,

        connectivity: int = DEFAULT_CONNECTIVITY,
        expansion_add: int = DEFAULT_EXPANSION_ADD,
        expansion_search: int = DEFAULT_EXPANSION_SEARCH,
        tune: bool = False,

        path: Optional[os.PathLike] = None,
        view: bool = False,
    ) -> None:
        """Construct the index and compiles the functions, if requested (expensive).

        :param ndim: Number of vector dimensions
        :type ndim: int

        :param metric: Distance function, defaults to MetricKind.IP
        :type metric: Union[MetricKind, Callable], optional
            Kind of the distance function, or the Numba `cfunc` JIT-compiled object.
            Possible `MetricKind` values: IP, Cosine, L2sq, Haversine, 
            Hamming, Tanimoto, Sorensen.
            Not every kind is JIT-able.

        :param dtype: Scalar type for internal vector storage, defaults to None
        :type dtype: str, optional
            For continuous metrics can be: f16, f32, f64, or f8.
            For bitwise metrics it's implementation-defined, and can't change.
            Example: you can use the `f16` index with `f32` vectors in Euclidean space,
            which will be automatically downcasted.

        :param jit: Enable Numba to JIT compile the metric, defaults to False
        :type jit: bool, optional
            This can result in up-to 3x performance difference on very large vectors
            and very recent hardware, as the Python module is compiled with high
            compatibility in mind and avoids very fancy assembly instructions.

        :param connectivity: Connections per node in HNSW, defaults to None
        :type connectivity: Optional[int], optional
            Hyper-parameter for the number of Graph connections
            per layer of HNSW. The original paper calls it "M".
            Optional, but can't be changed after construction.

        :param expansion_add: Traversal depth on insertions, defaults to None
        :type expansion_add: Optional[int], optional
            Hyper-parameter for the search depth when inserting new
            vectors. The original paper calls it "efConstruction".
            Can be changed afterwards, as the `.expansion_add`.

        :param expansion_search: Traversal depth on queries, defaults to None
        :type expansion_search: Optional[int], optional
            Hyper-parameter for the search depth when querying 
            nearest neighbors. The original paper calls it "ef".
            Can be changed afterwards, as the `.expansion_search`.

        :param tune: Automatically adjusts hyper-parameters, defaults to False
        :type tune: bool, optional

        :param path: Where to store the index, defaults to None
        :type path: Optional[os.PathLike], optional
        :param view: Are we simply viewing an immutable index, defaults to False
        :type view: bool, optional
        """

        if metric is None:
            metric = MetricKind.IP

        if isinstance(metric, Callable):
            self._metric_kind = MetricKind.Unknown
            self._metric_jit = metric
            self._metric_pointer = int(metric.address)

        elif isinstance(metric, MetricKind):
            if jit:
                self._metric_kind = metric
                self._metric_jit = jit_metric(
                    ndim=ndim,
                    metric_kind=metric,
                    dtype=dtype,
                )
                self._metric_pointer = self._metric_jit.address if \
                    self._metric_jit else 0
            else:
                self._metric_kind = metric
                self._metric_jit = None
                self._metric_pointer = 0
        else:
            raise ValueError(
                'The `metric` must be Numba callback or a `MetricKind`')

        if metric in BitwiseMetricKind:
            self._compiled = _CompiledBitsIndex(
                bits=ndim,
                metric=self._metric_kind,
                connectivity=connectivity,
                expansion_add=expansion_add,
                expansion_search=expansion_search,
            )
        else:
            if dtype is None:
                dtype = 'f32'
            self._compiled = _CompiledIndex(
                ndim=ndim,
                metric=self._metric_kind,
                metric_pointer=self._metric_pointer,
                dtype=dtype,
                connectivity=connectivity,
                expansion_add=expansion_add,
                expansion_search=expansion_search,
                tune=tune,
            )

        self.path = path
        if path and os.path.exists(path):
            if view:
                self._compiled.view(path)
            else:
                self._compiled.load(path)

    def add(
            self, labels, vectors, *,
            copy: bool = True, threads: int = 0):
        """Inserts one or move vectors into the index.

        For maximal performance the `labels` and `vectors`
        should conform to the Python's "buffer protocol" spec.

        To index a single entry: 
            labels: int, vectors: np.ndarray.
        To index many entries: 
            labels: np.ndarray, vectors: np.ndarray.

        When working with extremely large indexes, you may want to
        pass `copy=False`, if you can guarantee the lifetime of the
        primary vectors store during the process of construction.

        :param labels: Unique identifier for passed vectors.
        :type labels: Buffer
        :param vectors: Collection of vectors.
        :type vectors: Buffer
        :param copy: Should the index store a copy of vectors, defaults to True
        :type copy: bool, optional
        :param threads: Optimal number of cores to use, defaults to 0
        :type threads: int, optional
        """
        assert isinstance(vectors, np.ndarray), 'Expects a NumPy array'
        assert vectors.ndim == 1 or vectors.ndim == 2, 'Expects a matrix or vector'
        is_batch = vectors.ndim == 2
        generate_labels = labels is None

        # If no `labels` were provided, generate some
        if generate_labels:
            start_id = len(self._compiled)
            if is_batch:
                labels = np.arange(start_id, start_id + vectors.shape[0])
            else:
                labels = start_id
        if isinstance(labels, np.ndarray):
            labels = labels.astype(np.longlong)

        self._compiled.add(labels, vectors, copy=copy, threads=threads)

        if generate_labels:
            return labels

    def search(
            self, vectors, k: int = 10, *,
            threads: int = 0, exact: bool = False) -> Matches:
        """Performs approximate nearest neighbors search for one or more queries.

        :param vectors: Query vector or vectors.
        :type vectors: Buffer
        :param k: Upper limit on the number of matches to find, defaults to 10
        :type k: int, optional

        :param threads: Optimal number of cores to use, defaults to 0
        :type threads: int, optional
        :param exact: Perform exhaustive linear-time exact search, defaults to False
        :type exact: bool, optional
        :return: Approximate matches for one or more queries
        :rtype: Matches
        """
        tuple_ = self._compiled.search(
            vectors, k,
            exact=exact, threads=threads,
        )
        return Matches(*tuple_)

    def __len__(self) -> int:
        return len(self._compiled)

    @property
    def jit(self) -> bool:
        return self._metric_jit is not None

    @property
    def size(self) -> int:
        return self._compiled.size

    @property
    def ndim(self) -> int:
        return self._compiled.ndim

    @property
    def dtype(self) -> str:
        return self._compiled.dtype

    @property
    def connectivity(self) -> int:
        return self._compiled.connectivity

    @property
    def capacity(self) -> int:
        return self._compiled.capacity

    @property
    def memory_usage(self) -> int:
        return self._compiled.memory_usage

    @property
    def expansion_add(self) -> int:
        return self._compiled.expansion_add

    @property
    def expansion_search(self) -> int:
        return self._compiled.expansion_search

    @expansion_add.setter
    def change_expansion_add(self, v: int):
        self._compiled.expansion_add = v

    @expansion_search.setter
    def change_expansion_search(self, v: int):
        self._compiled.expansion_search = v

    def save(self, path: os.PathLike):
        self._compiled.save(path)

    def load(self, path: os.PathLike):
        self._compiled.load(path)

    def view(self, path: os.PathLike):
        self._compiled.view(path)

    def clear(self):
        self._compiled.clear()

    def remove(self, label: int):
        pass
