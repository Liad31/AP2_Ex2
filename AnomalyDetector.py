import clr
import os

from AnomalyDetection import SimpleAnomalyDetector,HybridAnomalyDetector, TimeSeries
import pandas as pd
import tempfile
class AnomalyDetector():
    def __init__(self, model, json):
        df=pd.read_json(json)
        with tempfile.NamedTemporaryFile() as tmp:
            tmp.write(df.to_csv(index=False).encode())
            tmp.seek(0)
            model.learnNormal(TimeSeries(tmp.name))
            self.Model = model

    def getAnomalySpan(self, json):
        df=pd.read_json(json)
        with tempfile.NamedTemporaryFile() as tmp:
            tmp.write(df.to_csv(index=False).encode())
            tmp.seek(0)
            arr = self.Model.detect(TimeSeries(tmp.name))
        if not arr:
            return []
        last = arr[0].timestamp
        first = arr[0]
        res = {}
        for i in range(1, len(arr) - 1):
            last += 1
            if last == arr[i].timestamp:
                continue
            col1, col2 = first.description.split(",", 1)
            # res.append({"span": f"[{first.timestamp},{last}]", "first": col1, "second": col2})
            res[col1]=res.get(col1,[])+[f"[{first.timestamp}, {last}]"]
            res[col2]=res.get(col2,[])+[f"[{first.timestamp}, {last}]"]
            first = arr[i]
            last = arr[i].timestamp
        last += 2
        col1, col2 = first.description.split(",", 1)
        res[col1] = res.get(col1, []) + [f"[{first.timestamp}, {last}]"]
        res[col2] = res.get(col2, []) + [f"[{first.timestamp}, {last}]"]
        return res
    def getCorrelatedFeatures(self):
        return self.Model.correlatedFeatures


class LinearAnomalyDetector(AnomalyDetector):
    def __init__(self, correctCsv):
        model = SimpleAnomalyDetector()
        super().__init__(model, correctCsv)


class CircleAnomalyDetector(AnomalyDetector):
    def __init__(self, correctCsv):
        model = HybridAnomalyDetector()
        super().__init__(model, correctCsv)

