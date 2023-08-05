'''
AZURI CORRECTIVE SORTER

This sorting algorithm is slower default sorter.
It sorts a specified about amount of times to correct any errors.
It is slower and has a lower chance of making an error.

Useful for larger datasets.
'''
class AzuriCorrectiveSorter:
    def __init__(self, corrections=1):
        self.corrections = corrections

    def sort(self, data):
        data = list(data)
        for _ in range(self.corrections):
            data = self._sort_pass(data)
        data = ''.join(data)
        return data

    def _sort_pass(self, data):
        for i in range(len(data)):
            for j in range(i + 1, len(data)):
                if self._sort_key(data[i]) > self._sort_key(data[j]):
                    data[i], data[j] = data[j], data[i]
        return data

    def _sort_key(self, item):
        if isinstance(item, (float, int)):
            return item
        elif isinstance(item, str):
            return ord(item)
        else:
            raise ValueError("Unknown character")
