#include <iostream>
#include "Display.h"
#include "Solver.h"
#include <QTest>

class TestQString : public QObject
{
    std::cout << "Starting Real-Time Trajectories application..." << std::endl;

    // Initialize the display
    Display display(800, 600, "Real-Time Trajectories");

    // Initialize the solver
    Solver solver;

    // Main loop
    while (!display.IsClosed())
    {
        // Clear the display
        display.Clear(0.0f, 0.15f, 0.3f, 1.0f);

        // Update the display
        display.Update();

        // Poll for events
        display.PollEvents();
    }

    return 0;
}

Q_OBJECT private slots : void
                         toUpper();
}
;

void TestQString::toUpper()
{
    QString str = "Hello";
    QVERIFY(str.toUpper() == "HELLO");
}

QTEST_MAIN(TestQString)