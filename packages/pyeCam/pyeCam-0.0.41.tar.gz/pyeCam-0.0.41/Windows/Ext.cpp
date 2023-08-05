#include <pybind11/pybind11.h>
#include <pybind11/functional.h>

namespace py = pybind11;

class Ext {
public:
    int init() {
        return 1;
    }

    int deinit() {
        return 1;
    }

    int initWrapper() {
        int result = init();
        // Perform any additional processing or error handling if needed
        return result;
    }

    int deinitWrapper() {
        int result = deinit();
        // Perform any additional processing or error handling if needed
        return result;
    }
};

PYBIND11_MODULE(Ext, m) 
{
    py::class_<Ext>(m, "Ext")
        .def("init", &Ext::initWrapper, "Initialize Ext")
        .def("deinit", &Ext::deinitWrapper, "Deinitialize Ext");
}
