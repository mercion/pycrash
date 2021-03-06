'''
PyCrash - A Run-Time Exception Dumper for Python Applications. 

PyCrash allows you to eayly add crash reporting facilities to
your python applications. It supports the gneraton of crash 
reports in both XML and HTML.

'''#
# (C)Copyright Carmine Ivan Delio Noviello 2003-2004 <cnoviello@pycrash.org>
#
# For further informations, please refer to: www.pycrash.org
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.

# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.

import logging
import types
import sys
import os
import string
import atexit
import time
import threading
import platform

from exctb import ExceptionTraceBack
from lxml import etree

from version import PYCRASH_VERSION
#_DictType = types.DictType
#_StringType = types.StringType
#del types

#_exc_info = sys.exc_info


#_StringLower = string.lower
#del string

#_atexit_register = atexit.register
#_atexit_exithandlers = atexit._exithandlers
#del atexit

#_time = time.time
#_localtime = time.localtime
#del time

#_currentThread = threading.currentThread
#del threading

#Global variables definition
PYCRASH_REFERENCE         = None

class PyCrash(object):
    '''
    This object is a singleon and when enabled will overided utilize
    the sys.exceptHook. 

    

    '''
    __initialized = 0  #initialization flag
    STATUS_ENABLED = 1 #PyCrash status flags
    STATUS_DISABLED = 0
    
    def __init__(self, **options):
        '''
        On initilaztion you can specify any number of options in the form of
        key=value. Valid options are ...

        :param:`AppName`: The Name of the Application. This is used for reporting
         purposes in the XML/HTML reports.

        :param:`Version`: The version of the Application. Used for reporting 
         purposes.

        :param:`SendTo`: Specifies where the XML crash report will be sent to. If
         the value starts with "email:" then the XML crash report will be emailed
         to the address. (eg SendTo = 'email:owner@application.com'). If the value
         starts with 'http:', then the xml crash report will be HTTP POSTed to the
         specified address (eg, SendTo = 'http://www.pycrash.org/ACR'). Note that
         autentication is currently not supported.

        :param:`time`: Specified when the application started. If not specified the
         current time is used.

        Note that the pycrash object must be a singleton and as such only one such
        object will exist per application. On initalization the singleton is sotred
        in the gloabl PYCRASH_REFERENCE. If a second pycrash object is intialized
        it will return the first one.

        '''
        self._AppName = options.get("AppName", "Not-Set")
        self._Version = options.get("Version", "0")
        self._SendTo = options.get("SendTo", "user@localhost")

        #TODO: We should do something intelegent to check what type of time the user
        # passes in
        self._time = options.get("time", time.time()) #When the application started
        self._dispatchers = []
    

        global PYCRASH_REFERENCE
            
        #A PyCrash object must be static (unique for the entiere application).
        #So we first check that this is the first istance
        if PYCRASH_REFERENCE is not None:
            return PYCRASH_REFERENCE
        #Then we check that if this object is just initialized
        if self.__initialized:
            return 
        
        self.__appCrashed = 0
        self.__status = self.STATUS_DISABLED
        self.__oldHook = None
        self.__numberOfExceptions = 0 #This is used to count the number of 
                                        #uncaught exceptions raised
        self.__tbList = [] #List of ExceptionThraceback objects
        self.__time = [self._time, None] #[0]=application started, [1]=exception raised
        self.__customRecords = []

        self.__initialized = 1 #The PyCrash object is now intialized

        #We set this variable in order to have an unique PyCrash object
        #for the application
        PYCRASH_REFERENCE = self
    
    def __exceptHook(self, type, value, tb):
        assert self.__initialized, "PyCrash.__init__() not called"

        
        if type is None and value is None and tb is None:
            return


        #Ok. Something is wrong and let's build the crush dump
        #This method is called each time an exception isn't caught. So
        #we must check that this is the first time
        if not self.__appCrashed:
            self.__appCrashed = 1
            self.__time[1] = time.time()
        
        #We fetch the reference to current thread to take its name
        t = threading.currentThread()
        self.__mkCrashDump(t.getName(), (type, value, tb))
        self.__numberOfExceptions += 1
        self.onExceptionRaised(self.__numberOfExceptions)

    def __exit(self): 
        assert self.__initialized, "PyCrash.__init__() not called"
        
        try:
            self.onExit()    
        except Exception, msg:
            print Exception, msg

    #def __getAppInfo(self):
    #    assert self.__initialized, "PyCrash.__init__() not called"
    #    
    #    strInfo = " appname=\"" + self._AppName + "\" appversion=\"" +  self._Version + "\"" 
    #    strInfo += " started=\"" + time.ctime(self.__time[0]) + "\" crashed=\"" + time.ctime(self.__time[1]) + "\""
    #    return strInfo
    #
    #def __getCustomRecords(self):
    #    assert self.__initialized, "PyCrash.__init__() not called"
    #    
    #    #FIXME: use lxml
    #    strInfo = ""
    #    for elem in self.__customRecords:
    #        strInfo += "\t<customrecord>" + elem + "</customrecord>\n"
    #
    #    return strInfo
    #
    #
    #def __getPythonInfo(self):
    #    assert self.__initialized, "PyCrash.__init__() not called"
    #    
    #    strInfo = " pyversion=\"" + str(sys.version_info) + "\""
    #    strInfo += " pyapiversion=\"" + str(sys.api_version) + "\""
    #    return strInfo
    #    
    def __mkCrashDump(self, thread, excInfo):
        #This is the routine which builds up the crash dump 
        assert self.__initialized, "PyCrash.__init__() not called"
        
        #Parsing each exception traceback
        self.__tbList.append(ExceptionTraceBack(thread, excInfo))

        #Lets create an xml crash dump and had it to the disatchers

        xml = self.getCrashDump()

        for dispatcher in self._dispatchers:
            dispatcher.dispatch(xml)
            

    def addCustomRecord(self, record):
        '''
        Custom records are optional bits of information that can be included
        in the crash report.
        '''       
        assert self.__initialized, "PyCrash.__init__() not called"
        self.__customRecords.append(record)

    def disable(self):
        """
            Disable PyCrash to trace raised exceptions
        """
        if self.__status == self.STATUS_ENABLED:
            sys.excepthook = self.__oldHook
            for elem in atexit._exithandlers:
                if elem[0] == self.__exit:
                    atexit._exithandlers.remove(elem)

            self.__status == self.STATUS_DISABLED

    def enable(self):
        """
            Enable PyCrash to trace raised exceptions
        """
        if self.__status == self.STATUS_DISABLED:
            #PyCrash works well only with Python 2.3 or later. So, before we
            #set appropriate hooks, we must check that this is the right version: if no,
            #no hooks are set to avoid abnormal terminations of the program
            if sys.version_info[0] >= 2 and sys.version_info[1] >= 3:
                #Hooks need for catch raised exception and application exit
                self.__oldHook = sys.excepthook
                sys.excepthook = self.__exceptHook
                atexit.register(self.__exit)
                self.__status = self.STATUS_ENABLED
            else:
                raise Exception("PyCrash can't work with this version of Python. Please, use Python 2.3 or higher")
        

    def forceDump(self):
        """forceDump() forces the creation of the crash dump, if an
           exception is raised. 
           forceDump() method can be very useful when an exception hasn't
           reached the top-level, but the user wants the same to make a 
           dump of the application context"""

        type, value, tb = sys.exc_info()
        self.__exceptHook(type, value, tb) #We force the creation of crash
                                           #dump with this call
    
    def getCrashDump(self):
        assert self.__initialized, "PyCrash.__init__() not called"
        
        if self.__appCrashed:
            return self.toXML()
        return None

    def getFileName(self):
        assert self.__initialized, "PyCrash.__init__() not called"
        
        try:
            return self.__fileName
        except:
            return None

    def getNumberOfRaisedExceptions(self):
        assert self.__initialized, "PyCrash.__init__() not called"
        
        return self.__numberOfExceptions

    def isCrashed(self):
        """ Returns 1 (true) if the application has been crashed, 
            otherwise 0 """
        assert self.__initialized, "PyCrash.__init__() not called"
        
        return self.__appCrashed

    def onBegin(self):
        """ User's defined actions: derived classes can override this
            method to add custom actions. This method is called at the 
            begin of crash dump construction """
        pass #User-defined actions

    def onEnd(self):
        """ User's defined actions: derived classes can override this
            method to add custom actions. This method is called at the end
            of crash dump construction """
        pass #User-defined actions
    
    def onExceptionRaised(self, time):
        """ User's defined actions: derived classes can override this
            method to add custom actions. This method is called every  
            time an uncaught exception is raised: "time" reports the number
            of uncaught exceptions raised """
        pass #User-defined actions

    def onExit(self):
        """ User's defined actions: derived classes can override this
            method to add custom actions. This method is called at the exit 
            of application """
        pass #User-defined actions
    
    def printErrorMessage(self, exception, message):
        assert self.__initialized, "PyCrash.__init__() not called"
        
        #TODO: this function should print something of more useful
        print exception, message


    def registerDispatcher(self, dispatcher):
        '''
        This method will register a dispatcher
        '''

        self._dispatchers.append(dispatcher)
    
    def saveToFile(self, filename):
        """ Save the crash dump file in a given 'filename' directory """
        assert self.__initialized, "PyCrash.__init__() not called"
        
        self.__fileName = filename
        
        if self.__appCrashed:
            fd = open(filename, "w")
            fd.write(self.getCrashDump())
            fd.close()

    def toXML(self):
        """ Returns the XML rapresentation of the crash dump """
        assert self.__initialized, "PyCrash.__init__() not called"

        crash = etree.Element("PyCrash", 
                    version=str(PYCRASH_VERSION),
                    appname=str(self._AppName),
                    appversion=str(self._Version),
                    started=time.ctime(self.__time[0]),
                    crashed=time.ctime(self.__time[1]),
                    duration=time.ctime(self.__time[0] - self.__time[1]),
                    osinfo=str(platform.platform()),
                    pyversion=str(sys.version_info),
                    pyapiversion=str(sys.api_version))

        for elem in self.__customRecords:
            record_element = etree.Element("customrecord")
            record_element.text = elem
            crash.append(record_element)
   
        for tb in self.__tbList:
            crash.append(tb.toXML())
                             
        return etree.tostring(crash, pretty_print=True)
