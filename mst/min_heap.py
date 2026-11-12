# -------------------------------------------------
# DO NOT CHANGE THIS FILE.
# Indexed binary min-heap (priority queue), provided for Prim's.
#
# Each entry is keyed, so a key appears at most once. When a cheaper
# priority arrives for a key already in the heap, its priority is
# lowered in place and the entry sifts up --- this is the decrease-key
# operation Prim's relies on.
#
# __author__ = 'Edward Small'
# __project__ = "Neuromancer: Hacking with Graphs"
# __copyright__ = 'Copyright 2026, RMIT University'
# -------------------------------------------------


class MinHeap:
    """
    An indexed binary min-heap (priority queue) of (priority, key, value)
    entries. Each key is stored at most once; a position map tracks where
    each key sits in the heap so its priority can be lowered in place.
    The entry with the smallest priority is always removed first.
    """

    def __init__(self) -> None:
        """
        Initialises an empty priority queue.

        @returns: None
        """
        self._heap: list = []            # list of [priority, key, value]
        self._pos: dict = {}             # key -> index in self._heap

    def __len__(self) -> int:
        """
        @returns: The number of entries currently in the queue.
        """
        return len(self._heap)

    def __contains__(self, key) -> bool:
        """
        @param key: The key to look for.
        @returns: True if an entry with this key is in the queue.
        """
        return key in self._pos

    def _swap(self, i: int, j: int) -> None:
        """
        Swaps two heap entries and updates the position map.

        @param i: First index.
        @param j: Second index.
        @returns: None
        """
        h = self._heap
        h[i], h[j] = h[j], h[i]
        self._pos[h[i][1]] = i
        self._pos[h[j][1]] = j

    def _sift_up(self, i: int) -> None:
        """
        Moves the entry at index i up while it is smaller than its parent.

        @param i: The index to sift up from.
        @returns: None
        """
        while i > 0:
            parent = (i - 1) // 2
            if self._heap[parent][0] <= self._heap[i][0]:
                break
            self._swap(parent, i)
            i = parent

    def _sift_down(self, i: int) -> None:
        """
        Moves the entry at index i down while a child is smaller.

        @param i: The index to sift down from.
        @returns: None
        """
        n = len(self._heap)
        while True:
            left, right, small = 2 * i + 1, 2 * i + 2, i
            if left < n and self._heap[left][0] < self._heap[small][0]:
                small = left
            if right < n and self._heap[right][0] < self._heap[small][0]:
                small = right
            if small == i:
                break
            self._swap(i, small)
            i = small

    def push(self, priority, key, value) -> None:
        """
        Inserts a new key with the given priority and value, sifting it
        up into place.

        @param priority: The comparable priority (smaller comes first).
        @param key: The unique key identifying this entry.
        @param value: Any payload carried with the entry.
        @returns: None
        """
        self._heap.append([priority, key, value])
        i = len(self._heap) - 1
        self._pos[key] = i
        self._sift_up(i)

    def decrease_key(self, key, priority, value) -> None:
        """
        Lowers the priority of an existing key and re-sifts it upward.
        Has no effect if the new priority is not smaller than the
        current one.

        @param key: The key whose priority is being lowered.
        @param priority: The new (smaller) priority.
        @param value: The payload to store alongside the new priority.
        @returns: None
        """
        i = self._pos[key]
        if priority >= self._heap[i][0]:
            return
        self._heap[i][0] = priority
        self._heap[i][2] = value
        self._sift_up(i)

    def pop(self):
        """
        Removes and returns the entry with the smallest priority as a
        (priority, key, value) tuple.

        @returns: A (priority, key, value) tuple.
        """
        h = self._heap
        top = h[0]
        last = h.pop()
        del self._pos[top[1]]
        if h:
            h[0] = last
            self._pos[last[1]] = 0
            self._sift_down(0)
        return tuple(top)
