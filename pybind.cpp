//
// Created by liad on 5/5/21.
//
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
namespace py=pybind11;
#include "AnomalyDetector.h"
#include "timeseries.h"
#include "SimpleAnomalyDetector.h"
#include "anomaly_detection_util.h"
#include "HybridAnomalyDetector.h"
PYBIND11_MODULE(AnomalyDetection, m) {
py::class_<Line>(m,"Line")
.def_readonly("a",&Line::a)
.def_readonly("b",&Line::b);
py::class_<AnomalyReport>(m, "AnomalyReport")
.def_readonly("timestamp", &AnomalyReport::timeStep)
.def_readonly("description",&AnomalyReport::description);
py::class_<TimeSeries>(m,"TimeSeries")
.def(py::init<const char *>())
.def("getAttributes",&TimeSeries::gettAttributes);
py::class_<correlatedFeatures>(m,"correlatedFeatures")
        .def_readonly("feature1",&correlatedFeatures::feature1)
        .def_readonly("feature2",&correlatedFeatures::feature2)
.def_readonly("corrlation",&correlatedFeatures::corrlation)
.def_readonly("linReg",&correlatedFeatures::lin_reg)
.def_readonly("cx",&correlatedFeatures::cx)
.def_readonly("cy",&correlatedFeatures::cy)
.def("__repr__",[](const correlatedFeatures &cf){
    return cf.feature1+","+ cf.feature2+","+ std::to_string(cf.corrlation);
})
.def(py::pickle([](const correlatedFeatures &cf) { // __getstate__
return py::make_tuple(cf.feature1, cf.feature2, cf.corrlation, cf.lin_reg.a,cf.lin_reg.b,cf.threshold,cf.cx,cf.cy);
},
[](py::tuple t) { // __setstate__
if (t.size()!=8 )
throw std::runtime_error("Invalid state!");
correlatedFeatures cf;
cf.feature1=t[0].cast<std::string>();
cf.feature2=t[1].cast<std::string>();
cf.corrlation=t[2].cast<float>();
Line l(t[3].cast<float>(),t[4].cast<float>());
cf.lin_reg=l;
cf.threshold=t[5].cast<float>();
cf.cx=t[6].cast<float>(); 
cf.cy=t[7].cast<float>();
return cf;
return cf;
}));
py::class_<SimpleAnomalyDetector>(m,"SimpleAnomalyDetector").def(py::init<>())
        .def("learnNormal",&SimpleAnomalyDetector::learnNormal)
        .def("detect",&SimpleAnomalyDetector::detect)
        .def_readonly("correlatedFeatures",&SimpleAnomalyDetector::cf)
        .def(py::pickle(
        [](const SimpleAnomalyDetector &p) { // __getstate__
            /* Return a tuple that fully encodes the state of the object */
            py::list res=py::cast(p.cf);
            return res;
        },
        [](py::list t) { // __setstate__
            SimpleAnomalyDetector sad;
            sad.cf=t.cast<vector<correlatedFeatures>>();
            return sad;
        }));
py::class_<HybridAnomalyDetector, SimpleAnomalyDetector>(m,"HybridAnomalyDetector")
        .def(py::init<>())
        .def(py::pickle(
        [](const HybridAnomalyDetector &p) { // __getstate__
            /* Return a tuple that fully encodes the state of the object */
            py::list res=py::cast(p.cf);
            return res;
        },
        [](py::list t) { // __setstate__
            HybridAnomalyDetector sad;
            sad.cf=t.cast<vector<correlatedFeatures>>();
            return sad;
        }));
}
