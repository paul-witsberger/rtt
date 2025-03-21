#include <boost/python.hpp>

std::string greet()
{
    return "Hello, world!";
}

BOOST_PYTHON_MODULE(pyrtt)
{
    boost::python::def("greet", greet);
}