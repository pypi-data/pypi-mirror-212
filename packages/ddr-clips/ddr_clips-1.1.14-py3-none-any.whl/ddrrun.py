########################################################################################
#
# ddrrun.py - Top level Python script used to run the  DDR  runtime main script.
#              This main script initializes the emre runtime state and starts the CLIPs runtime
#              environment.
#
#              ddrrun.py can be invoked with optional command line parameters described below:
#
#              ddrrun.py --facts=/path_to/facts --rules=/path_to/rules --flags=/path_to/flags --init=/path_to/initial-facts --tests=/path_to/test-facts --model=0 --runone=0

import os
from ddrclass import DDR
from optparse import OptionParser

def main():
    #
    # DDR accepts six files that define parameters used to control  DDR  execution
    # The files are defined as optional parameters.  If not parameter is provided when DDR is started
    # default file names are used assuming the files are located in the directory where runddr.py is started
    #
    #    facts - Initial configurations for DDR including:
    #                       initial_facts - Initial FACTs to assert when DDR is started
    #                       fact collection instructions - Instructions used by DDR runtime to collect FACT data from many sources
    #                       triggering events - Definitions of events used to trigger DDR execution in the main script
    #                       configurations - Definitions of configurations applied by RULEs when RULEs are executed
    #                       
    #
    #    rules - CLIPs "declarations" used to control runtime execution.  Declarations include "deffacts" which are initial FACTs
    #                       that can be loaded and then asserted when CLIPs is started.  "deftemplates" are definitions of the fields in FACTS.
    #                       "defrules" define the RULEs executed by CLIPs when FACTs are asserted that satisfy the RULE requirements
    #
    #    flags - control flags - Flags that control DDRexecution
    #
    #    devices - Devices used by use case
    #
    #    init - Optional file containing additional FACTs defined in CLIPs format that can be asserted by DDR on startup
    #
    #    tests - DDR can be run using simulated FACTs instead of collecting FACT data from devices.  Simulated FACTs can be used
    #                            test workflows including failure paths which would be difficult to create on an actual network.  A set of test FACTs
    #                            are asserted each time the  DDR  main script runs through a cycle
    #
    # Additional command line options
    #
    #    model(0) - If the model parameter is set to 1,  DDR  will use the cisco-ios-xe-ddr-control.yang model to load the content defined in the "facts" file above
    #    runone(0) - If set to 1, the main  DDR  script will run through one cycle then exit
    #
    # Read optional command line arguments for set defaults
    #
    parser = OptionParser('')
    parser.add_option("--facts", dest="facts", type="string", default='ddr-facts',
                      help="Relative path to the file containing instructions for collecting FACTS: default: ddr-facts")
    parser.add_option("--rules", dest="rules", type="string", default='ddr-rules',
                      help="Relative path to the file containing the RULES: default: ddr-rules")
    parser.add_option("--flags", dest="flags", type="string", default='ddr-flags',
                      help="Relative path to the file containing control flags: default: ddr-flags")
    parser.add_option("--devices", dest="devices", type="string", default='ddr-devices',
                      help="Relative path to the file containing use case devices: default: ddr-devices")
    parser.add_option("--tests", dest="tests", type="string", default='ddr-tests',
                      help="Relative path to the file containing the test facts: default: ddr-tests")
    parser.add_option("--init", dest="init", type="string", default='ddr-init',
                      help="Relative path to the file containing the initial-facts file: default: ddr-init")
    parser.add_option("--control", dest="control", type="string", default='ddr-control',
                      help="Relative path to the file containing the external application control file: default: ddr-control")
    parser.add_option("--sim", dest="sim", type="string", default='ddr-sim',
                      help="Relative path to the file containing the simulated facts for rule execution file: default: ddr-sim")
    parser.add_option("--parsers", dest="parsers", type="string", default='ddrparsers.py',
                      help="Relative path to the file containing any special parsers required for the usecase: default: ddrparsers.py")
    parser.add_option("--model", dest="model", type=int, default=0,
                      help="Set to 1 to use ddr-control model")
    parser.add_option("--runone", dest="runone", type=int, default=0,
                      help="Set to 1 to stop  DDR  after one execution cycle")

    (o, args) = parser.parse_args()
    factsfile = o.facts
    rulesfile = o.rules
    flagsfile = o.flags
    devicesfile = o.devices
    testsfile = o.tests
    initfacts = o.init
    controlfile = o.control
    simfile = o.sim
    parserfile = o.parsers
    model_control = o.model
    run_one = o.runone
    #
    # Run the main  DDR  script
    #
    try:
        flist = [factsfile, rulesfile, flagsfile, devicesfile, testsfile, initfacts, controlfile, simfile, parserfile]
    #
    # Create instance of ddr class
    # 
        engine = DDR()
    #
    # Start DDR passing a the list of configuration files, whether to use model control and a single execution flag
    #
        engine.ddr(flist, model_control, run_one)
    except Exception as e:
        print("%%%%% DDR Execution Terminated: " + str(e))

if __name__ == "__main__":
    main()
