********************
Introduction
********************

Introduction to PyCrash
===================================

PyCrash is a Python Application Crash Reporting service that
allows you to easily add in Crash Reporting to you python applications. When
PyCrash is enabled, if your python application crashes then you will get an
XML crash report containing the following information:
    * All the stack frames that were running
    * All the variables and definitions for that stack frame
    * Full Exception Traceback.

For an example crash report see example_report.xml. However in addition to this
PyCrash can also generate a HTML crash report from the XML crash report. You can
see an example of such a report here example-html-crash-report.html.

PyCrash also has a notion of dispatchers. When a crash report is generated it is
sent to all of the registered dispatchers. The dispatchers will then send that
crash report to the appropriate location. The built in dispatchers are :
    * :class:`pycrash.dispatchers.XMLMailDispatcher` 
        This dispatcher will take the XML crash dump  and generate and email
        message. The body of the email message will contain a summary of the
        crash dump, with the full XML report being attached to the email.

    * :class:`pycrash.dispatchers.HTMLMailDispatcher`
        This dispatcher will take the XML crash report and generate a HTML crash 
        report. This html crash report will then be  sent as an email to the 
        :param:to_address. The XML report will also be attached to this email.

    * :class:`pycrash.dispatchers.XMLPostDispatcher`
        This dispatcher will take the xml_report and then submit
        a HTTP POST request to the :pram:target_uri. The body of the POST
        message will contain the XML crash report. 

For more information on dispatchers and how to create your own dispatcher see
the dispatchers section.


Also have a look at "PACeR". It is a simple python application crash reporting server
that has been written specifically for PyCrash crash reports. You can configure
PyCrash to send its crash report to PACeR and it will keep track of all the
crash reports. 

