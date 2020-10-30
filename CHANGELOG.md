
# Changelog

## version v0.0.8

- PEP8
- added `__app__.py` for auto discovery and auto configuration (new feature in modcore v0.0.17)
- proper testing pending. due to winter season the watering prototype is not running in the garden 
- `__app__.py` obsoletes `modapp.watering.boot.py`
- 


## BACKLOG

- valve config module, program pos shifting tbi
- add auto restart module
- valve direct control module
- program module
- schedule module
- scheduler module (which program to run)
- program flow -> do refresh automatically (present: manual trigger with button)
- refactor using vuex (?)
- status bar, error handling
- add flow measure module (stop watering when bounds exceed)
- add pump module
- refactor ui design, and allignment
- form input validation
- add environment sensor(s) eg temperature, barometer, ...
- refactor system info also as app (own project on github)
- refactor authorization (eg only admin can change settings)
- refactor to fiber (if required)
- refactor imports
- 


## version v0.0.7

- bug fixes
- status bar / notifications dialog on tab bar
- minimalistic error reporting as status bar notification
- 

## version v0.0.6

- bug fixes
- smaller ui changes
- 


## version v0.0.5

- flow meter sensor draft implemenation 
-


## version v0.0.4

- due to bug in setup.py
- 


## version v0.0.3 (initial version)

- created initial skeleton and app base
- remark: this needs to be build against master branch of `mpy-modcore`
- most of the features (backlog) are implemented but in-deep testing is pending
- 

