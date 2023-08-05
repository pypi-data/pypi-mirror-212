'''
AZURI SORTER

This sorting algorithm is the default sorter.
It sorts twice to correct any errors.

Useful for medium sized datasets.
'''
class AzuriSorter:
    #Default sorter for Azuri
    def __init__(self):
        pass
    
    def loadset(self, file):
        #Return a dataset
        with open(file, 'r') as f:
            return f.read()
    
    def sort(self, data):
        #Sort the data
        data = list(data)
        data = self._first_pass_sort(data)
        data = self._second_pass_sort(data)
        data = ''.join(data)
        return data
    
    def _first_pass_sort(self, data):
        # First run through of sorting
        for i in range(len(data)):
            for j in range(i + 1, len(data)):
                try:
                    if self._sort_key(data[i]) > self._sort_key(data[j]):
                        data[i], data[j] = data[j], data[i]
                except ValueError as e:
                    print(f"Unknown character encountered at position {i}:", e)
        return data
    
    def _second_pass_sort(self, data):
        # Second run through of sorting
        for i in range(len(data)):
            for j in range(i + 1, len(data)):
                try:
                    if self._sort_key(data[i]) == self._sort_key(data[j]) and data[i] > data[j]:
                        data[i], data[j] = data[j], data[i]
                except ValueError as e:
                    print(f"Unknown character encountered at position {i}:", e)
        return data
    
    def _sort_key(self, item):
        # Sort based on ASCII Key
        if isinstance(item, (float, int)):
            return item, item
        elif isinstance(item, str):
            return ord(item), item
        else:
            raise ValueError("Unknown character")
