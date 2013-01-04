<!---

This mako template will take a XML pycrash dump and 
generate a HTML page displaying the information in 
the xml dump.

Author: Mercion Wilathgamuwage
--!>
<html>
<HEAD>
<style>

#main {
    margin: 0 auto;
    width: 800px; /* Replace the xxxx with the the width of your site (eg
800px)*/
    text-align:left;
    padding-top: 50px;
}
body {
    text-align: center;
    margin: 0 auto;
}
dl {
/*  border: 3px double #ccc;*/
    padding: 0.5em;
} 
dt {
    float: left;
    clear: left;
    width: 260px;
    text-align: right;
    font-weight: bold;
    padding-right: 5px;
    color: #87AAAE;
    font: bold 1em/1.5em "Helvetica Neue", Arial, Helvetica, Geneva, sans-serif;
    
}
dt::after {
    content: ":";
    padding-right: 5px;
}
dd {
    margin: 0 0 0 110px;
    padding-left: 5px;
    font: bold 1em/1.5em "Helvetica Neue", Arial, Helvetica, Geneva, sans-serif;
}

/*table {
    border: 1px solid #87AAAE;
    width: 900px;
    background-color: #F6F6F6 ;
}*/

div.pad {
    background-color: #87AAAE;
    text-align: center;
    width: 920px;
    padding-top: 0.7px;
    margin-bottom: 20px ;
    font: bold 1.2em/1.7em "Helvetica Neue", Arial, Helvetica, Geneva,
sans-serif;
    
}


table.crash {
    
    border: 1px solid #87AAAE;
    width: 900px;
    background-color: #F6F6F6;
}

td.exctb_blurb {
    font: bold 1em/1.5em "Helvetica Neue", Arial, Helvetica, Geneva, sans-serif;
}

table.exctb {
    width: 100%;
}

h2 {
    font: bold 1em/1.5em "Helvetica Neue", Arial, Helvetica, Geneva, sans-serif;
    padding-left: 20px;
}

table.varframe {
    width: 80%;
    border-collapse: collapse;
    border: 1px solid #333;
}

td.varframe, tr.varframe {
    border: 1px solid #333;
}



</style>

</HEAD>

<BODY>
<div id="main">
<div class="pad">
<p class="pad">
    PACR: PyCrash Application Crash Report
</p>
</div>
<table class="crash">
    <tr class="crash">
        <td class="crash">
            <dl class="crash">
                <dt>Application Name</dt>
                <dd>${crash.get("appname")}</dd>

                <dt>Application Version</dt>
                <dd>${crash.get("appversion")}</dd>

                <dt>Application Started</dt>
                <dd>${crash.get("started")}</dd>

                <dt>Application Crashed</dt>
                <dd>${crash.get("crashed")}</dd>

                <dt>Application Run Time</dt>
                <dd>${crash.get("duration")}</dd>

                <dt>Operating System Information</dt>
                <dd>${crash.get("osinfo")}</dd>

    
                <dt>Python Version</dt>
                <dd>${crash.get("pyversion")}</dd>

                <dt>Python API Version</dt>
                <dd>${crash.get("pyapiversion")}</dd>
            </dl>  
        <td>
    </tr>
    % for tb in crash:
    <tr class="crash" ><td class="crash">
        <table class="exctb">
            <tr class="exctb" >
                <td>
                    <hr />
                    <H2>Exception Traceback </H2>
                    <dl>
                        <dt>Thread Name</dt>
                        <dd>Main Thread -X-</dd>

                        <dt>Exception Type:</dt>
                        <dd>${tb.get("exctype")}</dd>

                        <dt>Exception Value:</dt>
                        <dd>${tb.get("value")}</dd>
                    </dl>
                </td>
            </tr>

            <tr class="exctb">
                <td class="exctb">
                    % for stack in tb:
                        <H2> Stackframe Details </H2>
                        <dl class="stackframe">
                            <dt>Frame Name</dt>
                            <dd>"FrameName"</dd>

                            <dt>Arg Count:</dt>
                            <dd>${stack.get("argcout")}</dd>

                            <dt>Size:</dt>
                            <dd>${stack.get("size")}</dd>

                            <dt>File Name:</dt>
                            <dd>${stack.get('filename')}</dd>

                            <dt>Line No:</dt>
                            <dd>${stack.get("line")}</dd>
                        </dl>
                        <div align="center"> 
                        <table class="varframe" >
                            <tr class="varframe">
                                <th class="varframe" > Variable Name </th>
                                <th class="varframe"> Variable Type </th>
                                <th class="varframe"> Variable Value </th>
                            <tr>
                            % for var in stack:
                                <tr class="varframe" >
                                    <td class="varframe" >${var.get("name")}</td>
                                    <td class="varframe" >${var.get("type")}</td>
                                    <td class="varframe" >${var.text}</td>
                                </tr>
                            % endfor
                        </table>
                        </div>
                    % endfor
                </td>
            </tr>
        </table>
    </td></tr>
    % endfor
</table>
</div>
</BODY>
</HTML>
