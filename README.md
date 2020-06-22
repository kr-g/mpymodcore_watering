
# mpymodcore_watering

a garden/ plant watering app for [`mpy-modcore`](https://github.com/kr-g/mpymodcore)


# What's new ?

Check
[`CHANGELOG`](https://github.com/kr-g/mpymodcore_watering/blob/master/CHANGELOG.md)
for latest ongoing, or upcoming news


## Development status

Alpha state. 
The API or logical call flow might change without prior notice.

In case your code breaks between two versions check
[`CHANGELOG`](https://github.com/kr-g/mpymodcore_watering/blob/master/CHANGELOG.md)
information first before creating a ticket / issue on github. thanks.


# Hardware, plumbing installation pictures and videos

refer docs on [`GitHub-Pages`](https://kr-g.github.io/mpymodcore_watering/)


# Required related project(s)

`mpymodcore_watering` requires [`mpy-modcore`](https://github.com/kr-g/mpymodcore)
in order to run



# Installation

assuming your repo structure as following
    
- ~/repo/mpymodcore
- ~/repo/mpymodcore_watering

install [`mpy-modcore`](https://github.com/kr-g/mpymodcore)
first (see installation notes there)

install to the mpymodcore_watering (project) folder
    
    `python3 -m pip install mpymodcore-watering --no-compile --target .` 
     
create a symbolic link in ~/repo/mpymodcore/modapp
    
    ln -sr ~/repo/mpymodcore_watering/modapp/watering watering

enable wlan on your esp32 board (with `wlan.cfg` file on the board)
since the web application loads external content from CDNs
such as bootstrap, fontawesome, vuejs, jquery, ... etc

in module `modapp.watering` there is a minimal `boot.py` script.

deploy the source files to the target board using e.g. thonny, mpycntrl, mpfshell, rshell, ...


# Basis Configuration

the default port/pin mapping is in `/modapp/watering/etc/valves.template.json.txt`.
this is used as template if on the board the file `/etc/watering/valves.json.txt`
is not found. make sure that the target board supports the defined pins.

the boot-button (gpio 0) is configured to send a break event to enter repl
securely after pressing. with calling `loop()` the stopped process can be
continued. check if the target board is configured like that.

the on-board led (gpio 21) will toggle every 5 sec as live ping.
check if the target board is configured like that.


# URL - read properly

access the application with `http://your-device-ip/static/watering/`
(important: trailing '/' in url above loads '/index.html' under given route path)


# License

`mpymodcore_watering` is published as
[`dual licensed`](https://github.com/kr-g/mpymodcore_watering/blob/master/LICENSE).
read properly.
    
## other Licenses

|Component  |Homepage   |License|
|---|---|---|
mpymodcore| https://github.com/kr-g/mpymodcore| dual licensed | 
fontawesome| https://fontawesome.com/| MIT | 
bootstrap| https://getbootstrap.com/| MIT | 
jQuery| https://jquery.com/| MIT | 
Popper| https://popper.js.org|      MIT | 
vuejs| https://vuejs.org/| MIT | 


