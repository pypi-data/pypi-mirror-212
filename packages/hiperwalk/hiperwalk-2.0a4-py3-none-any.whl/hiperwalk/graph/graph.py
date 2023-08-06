import numpy as np

def _binary_search(v, elem, start=0, end=None):
    r"""
    expects sorted array and executes binary search in the subarray
    v[start:end] searching for elem.
    Return the index of the element if found, otherwise returns -1
    Cormen's binary search implementation.
    Used to improve time complexity
    """
    if end == None:
        end = len(v)
    
    while start < end:
        mid = int((start + end)/2)
        if elem <= v[mid]:
            end = mid
        else:
            start = mid + 1

    return end if v[end] == elem else -1

class Graph():
    r"""
    Graph on which a quantum walk occurs.

    Used for generic graphs.

    Parameters
    ----------
    adj_matrix : :class:`scipy.sparse.csr_array`
        Adjacency matrix of the graph on
        which the quantum walk occurs.

    Raises
    ------
    TypeError
        if ``adj_matrix`` is not an instance of
        :class:`scipy.sparse.csr_array`.

    Notes
    -----
    Makes a plethora of methods available.
    These methods may be used by a Quantum Walk model for
    generating a valid walk.

    This class may be passed as argument to plotting methods.
    Then the default representation for the specific graph will be shown.

    The recommended parameter type is
    :class:`scipy.sparse.csr_array` using ``dtype=np.int8``
    with 1 denoting adjacency and 0 denoting non-adjacency.
    If any entry is different from 0 or 1,
    some methods may not work as expected.

    Each edge of a given graph :math:`G(V, E)`
    is associated with two arcs in the graph :math:`\vec{G}(V, A)`
    where

    .. math::
        \begin{align*}
            A = \bigcup_{(v,u) \in E} \{(v, u), (u, v)\}.
        \end{align*}

    Each arc has a label (number).
    The labels are ordered as follows.
    Let :math:`(v_1, u_1)` and :math:`(v_2, u_2')`
    be arcs with labels :math:`a_1` and :math:`a_2`, respectively.
    Then :math:`a_1 < a_2` if and only if
    if either :math:`v_1 < v_2` or
    :math:`v_1 = v_2` and :math:`u_1 < u_2`.

    .. note::
        The arc ordering may change for specific graphs.

    For example, the graph :math:`G(V, E)` shown in
    Figure 1 has adjacency matrix ``adj_matrix``.

    .. testsetup::

        import numpy as np

    >>> adj_matrix = np.array([
    ...     [0, 1, 0, 0],
    ...     [1, 0, 1, 1],
    ...     [0, 1, 0, 1],
    ...     [0, 1, 1, 0]])
    >>> adj_matrix
    array([[0, 1, 0, 0],
           [1, 0, 1, 1],
           [0, 1, 0, 1],
           [0, 1, 1, 0]])

    .. graphviz:: ../../graphviz/graph-example.dot
        :align: center
        :layout: neato
        :caption: Figure 1

    The corresponding arcs are

    >>> arcs = [(i, j) for i in range(4)
    ...                for j in range(4) if adj_matrix[i,j] == 1]
    >>> arcs
    [(0, 1), (1, 0), (1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2)]

    Note that ``arcs`` is already sorted, hence the labels are

    >>> arcs_labels = {arcs[i]: i for i in range(len(arcs))}
    >>> arcs_labels
    {(0, 1): 0, (1, 0): 1, (1, 2): 2, (1, 3): 3, (2, 1): 4, (2, 3): 5, (3, 1): 6, (3, 2): 7}

    The arcs labels are illustrated in Figure 2.

    .. graphviz:: ../../graphviz/graph-arcs.dot
        :align: center
        :layout: neato
        :caption: Figure 2

    If we substitute the arcs labels into the adjacency matrix,
    we obtain the matrix ``adj_labels``.

    >>> adj_labels = [[arcs_labels[(i,j)] if (i,j) in arcs_labels
    ...                                   else '' for j in range(4)]
    ...               for i in range(4)]
    >>> adj_labels = np.matrix(adj_labels)
    >>> adj_labels
    matrix([['', '0', '', ''],
            ['1', '', '2', '3'],
            ['', '4', '', '5'],
            ['', '6', '7', '']], dtype='<U21')

    Note that, intuitively,
    the arcs are labeled in left-to-right top-to-bottom fashion.

    .. todo::
        * Check if valid adjacency matrix
        * Add option: numpy dense matrix as parameters.
        * Add option: networkx graph as parameter.
    """

    def __init__(self, adj_matrix):
        self.adj_matrix = adj_matrix
        self.coloring = None

    def default_coin(self):
        r"""
        Returns the default coin for the given graph.

        The default coin for the coined quantum walk on general
        graphs is ``grover``.
        """
        return 'grover'

    def embeddable(self):
        r"""
        Returns whether the graph can be embedded on the plane or not.

        If a graph can be embedded on the plane,
        we can assign directions to edges and arcs.

        Notes
        -----
        The implementation is class-dependent.
        We do not check the graph structure to determine whether
        it is embeddable or not.
        """
        return False

    def arc_label(self, tail, head):
        r"""
        Returns arc label (number).

        Parameters
        ----------
        tail: int
            Tail of the arc.

        head: int
            Head of the arc.

        Returns
        -------
        label: int
            Arc label.
        """
        return _binary_search(self.adj_matrix.indices, head,
                              start = self.adj_matrix.indptr[tail],
                              end = self.adj_matrix.indptr[tail + 1])

    def arc(self, label):
        r"""
        Arc in arc notation.

        Given the arc label,
        returns it in the ``(tail, head)`` notation.

        Parameters
        ----------
        label: int
            Arc label (number)

        Returns
        -------
        (int, int)
            Arc in the arc notation ``(tail, head)``.
        """
        adj_matrix = self.adj_matrix
        head = adj_matrix.indices[label]
        # TODO: binary search
        for tail in range(len(adj_matrix.indptr)):
            if adj_matrix.indptr[tail + 1] > label:
                break
        return (tail, head)

    def next_arc(self, arc):
        r"""
        Next arc in an embeddable graph.

        Parameters
        ----------
        arc
            The arc in any of the following notations.

            * arc notation: tuple of vertices
                In ``(tail, head)`` format where
                ``tail`` and ``head`` must be valid vertices.
            * arc label: int.
                The arc label (number).

        Returns
        -------
        Next arc in the same notation as the ``arc`` argument.

        See Also
        --------
        arc
        arc_label
        """
        # implemented only if is embeddable
        raise AttributeError

    def previous_arc(self, arc):
        r"""
        Previous arc in an embeddable graph.

        Parameters
        ----------
        arc
            The arc in any of the following notations.

            * arc notation: tuple of vertices
                In ``(tail, head)`` format where
                ``tail`` and ``head`` must be valid vertices.
            * arc label: int.
                The arc label (number).

        Returns
        -------
        Previous arc in the same notation as the ``arc`` argument.

        See Also
        --------
        arc
        arc_label
        """
        # implemented only if is embeddable
        raise AttributeError

    def neighbors(self, vertex):
        r"""
        Returns all neighbors of the given vertex.
        """
        start = self.adj_matrix.indptr[vertex]
        end = self.adj_matrix.indptr[vertex + 1]
        return self.adj_matrix.indices[start:end]

    def arcs_with_tail(self, tail):
        r"""
        Returns all arcs that have the given tail.
        """
        arcs_lim = self.adj_matrix.indptr
        return np.arange(arcs_lim[tail], arcs_lim[tail + 1])

    def number_of_vertices(self):
        r"""
        Cardinality of vertex set.
        """
        return self.adj_matrix.shape[0]

    def number_of_arcs(self):
        r"""
        Cardinality of arc set.

        For simple graphs, this is twice the number of edges.
        """
        return self.adj_matrix.sum()

    def number_of_edges(self):
        r"""
        Cardinality of edge set.
        """
        return self.adj_matrix.sum() >> 1

    def degree(self, vertex):
        r"""
        Degree of given vertex.
        """
        indptr = self.adj_matrix.indptr
        return indptr[vertex + 1] - indptr[vertex]
