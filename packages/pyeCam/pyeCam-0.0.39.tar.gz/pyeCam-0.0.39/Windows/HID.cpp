#include <pybind11/pybind11.h>
#include <pybind11/functional.h>

namespace py = pybind11;

class HID {
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

PYBIND11_MODULE(HID, m) 
{
    py::class_<HID>(m, "HID")
        .def("init", &HID::initWrapper, "Initialize HID")
        .def("deinit", &HID::deinitWrapper, "Deinitialize HID");
}
