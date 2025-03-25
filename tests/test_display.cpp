#define BOOST_TEST_MODULE DisplayTest
#include <boost/test/unit_test.hpp>
#include "Display.h"

BOOST_AUTO_TEST_CASE(DisplayTest)
{
    Display display(800, 600, "Test Window");
    // Example assertions
    BOOST_CHECK_EQUAL(display.IsClosed(), false);
    display.Close();
    BOOST_CHECK_EQUAL(display.IsClosed(), true);
}

BOOST_AUTO_TEST_CASE(DisplayClear)
{
    Display display(800, 600, "Real-Time Trajectories");
    // Example assertion
    BOOST_REQUIRE_NO_THROW(display.Clear(0.0f, 0.15f, 0.3f, 1.0f));
}