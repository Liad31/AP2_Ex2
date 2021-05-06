import clr
import os

from AnomalyDetection import SimpleAnomalyDetector,HybridAnomalyDetector, TimeSeries


class AnomalyDetector():
    def __init__(self, model, csvPath):
        model.learnNormal(TimeSeries(csvPath))
        self.Model = model
        with open(csvPath) as file:
            self.VariablesChecked = file.readline()

    def getAnomalySpan(self, path):
        arr = self.Model.detect(TimeSeries(path))
        if not arr:
            return []
        last = arr[0].timestamp
        first = arr[0]
        res = []
        for i in range(1, len(arr) - 1):
            last += 1
            if last == arr[i].timestamp:
                continue
            col1, col2 = first.description.split(",", 1)
            res.append({"span": f"[{first.timestamp},{last}]", "first": col1, "second": col2})
            first = arr[i]
            last = arr[i].timestamp
        last += 2
        col1, col2 = first.description.split(",", 1)
        res.append({"span": f"[{first.timestamp},{last}", "first": col1, "second": col2})
        return res


class LinearAnomalyDetector(AnomalyDetector):
    def __init__(self, correctCsv):
        model = SimpleAnomalyDetector()
        super().__init__(model, correctCsv)


class CircleAnomalyDetector(AnomalyDetector):
    def __init__(self, correctCsv):
        model = HybridAnomalyDetector()
        super().__init__(model, correctCsv)

