soakdb3
=======================================================================

XChem replacement for soakdb2, including a new database backend.

repositories
------------------------------------------------------------------------
There are two repositories involved.  The first is this one, soakdb3.  This is where the code is, both front end and back end. It is on the public github.

The second one is soakdb3_configuration.  This has the specific runtime configuration for the processes.  It is on the Diamond gitlab.

front end
------------------------------------------------------------------------
Front-end runtime is two Excel spreadsheets.  These are deployed in the shared filesystem.

The front-end spreadsheet is started from soakdb3.bat in the visit directory.  The soakdb3.bat master copy is deployed in the shared filesystem as well.

To deploy a new version of the front-end, you cd to the soakdb3_configuration folder and type "make deploy_spreadsheets"

Development - Starting the Back End
------------------------------------------------------------------------

Furthermore, assume you have checked out the test data into c:\27\soakdb3.

    cd soakdb3
    pip install -e .
    soakdb3.cli start_services --c configurations/development.yaml



Development - Starting the Front End
------------------------------------------------------------------------

Assume you have checked out this repo into the folder c:\27\soakdb3.
Furthermore, assume you have checked out the test data into c:\27\soakdb3_test_data.

To run the spreadsheet on a development computer::

    set SOAKDB3_VISITID=c:\27\soakdb3_test_data\lb19758-64\processing\lab36\..
    set SOAKDB3_CONFIGFILE=c:\27\soakdb3\src\soakdb3_xls\excel_config.json
    start excel /x c:\27\soakdb3\src\soakdb3_xls\soakDB_v3.0.xlsm

To open the spreadsheet without running the initialization code so you can edit it::

    set SOAKDB3_EDITABLE=yes

..
    Anything below this line is used when viewing README.rst and will be replaced
    when included in index.rst



Documentation
-----------------------------------------------------------------------

See https://diamondlightsource.github.io/soakdb3 for more detailed documentation.

