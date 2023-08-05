'''
AZURI FAST SORTER

This sorting algorithm is faster than the default sorter.
It only sorts once and is optimized for speed.

Useful for small datasets.
'''
class AzuriFastSorter:
    def sort(self, data):
        data = list(data)
        self._quick_sort(data, 0, len(data) - 1)
        data = ''.join(data)
        return data

    def _quick_sort(self, data, low, high):
        if low < high:
            pivot_index = self._partition(data, low, high)
            self._quick_sort(data, low, pivot_index - 1)
            self._quick_sort(data, pivot_index + 1, high)

    def _partition(self, data, low, high):
        pivot = data[high]
        i = low - 1
        for j in range(low, high):
            if self._sort_key(data[j]) <= self._sort_key(pivot):
                i += 1
                data[i], data[j] = data[j], data[i]
        data[i + 1], data[high] = data[high], data[i + 1]
        return i + 1

    def _sort_key(self, item):
        if isinstance(item, (float, int)):
            return item
        elif isinstance(item, str):
            return ord(item)
        else:
            raise ValueError("Unknown character")
    def _reRun(self, data):
        data = list(data)
        self._quick_sort(data, 0, len(data) - 1)
        data = ''.join(data)
        return data