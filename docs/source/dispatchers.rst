dispatchers
=========================================

Dispatchers are responsible for taking an XML crash report and doing 
anything that is post crash report related. 


Enabling a dispatcher
----------------------

To enable a dispatcher you simply import the require dispatcher from 
:class:pycrash.dispatchers, configure it and then register it with 
your pycrash instance. 

Here is an example were we register the HTMLMailDispatcher::


    from pycrash import PyCrash
    from pycrash.dispatchers import HTMLMailDispatcher

    class SimpleCalculator:
    
        def add(a, b):
            return a + b

        def subtract(a, b):
            return a - b

    if __name__ == "__main__":
    
        crash_handler = PyCrash()
        email_dispatcher =  HTMLMailDispatcher("pycrash@SimpleCalc.com",
                                               "youremail@yourcompany.com",
                                               "outbound.gmail.com")
        crash_handler.register_dispatcher(email_dispatcher)

        crash_handler.enable()

        calc = SimpleCalculator()
        calc.add(1, 2)
        calc.add(1. "1.0")
        

Createing your own dispatcher
-----------------------------

Creating your own dispatcher is dead simple. Simply inherit from
:class:pycrash.dispatchers.BaseDispatcher and the define your actions
within a dispatch method. PyCrash will then call your dispatcher's dispatch
method with the xml_report being passed in as a string.

To illustrate lets extend the above example with a custom dispatcher that
prints out the XML report::

    from pycrash import PyCrash
    from pycrash.dispatchers import HTMLMailDispatcher
    from pycrash.dispatchers import BaseDispatcher

    class PrintDispatcher(BaseDispatcher):
        def dispatch(xml_report):
            print xml_report

    class SimpleCalculator:
    
        def add(a, b):
            return a + b

        def subtract(a, b):
            return a - b

    if __name__ == "__main__":
    
        crash_handler = PyCrash()
        email_dispatcher =  HTMLMailDispatcher("pycrash@SimpleCalc.com",
                                               "youremail@yourcompany.com",
                                               "outbound.gmail.com")

        print_dispatcher = PrintDispatcher()
        crash_handler.register_dispatcher(email_dispatcher)
        crash_handler.register_dispatcher(print_dispatcher

        crash_handler.enable()

        calc = SimpleCalculator()
        calc.add(1, 2)
        calc.add(1. "1.0")
        

