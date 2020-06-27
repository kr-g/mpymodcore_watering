
# Media files for <a href="https://github.com/kr-g/mpymodcore_watering">https://github.com/kr-g/mpymodcore_watering</a>


## Hardware:

  Recommended: Magnetic Valve 12V, NC (normal closed), plus plumbing, and garden watering adapters.

  <img width="640"
      src="https://github.com/kr-g/mpymodcore_watering/raw/master/docs/media/valves_mounted.jpg"
    />


## Valve in action:

  <video width="640" height="480" controls>
    <source src="https://github.com/kr-g/mpymodcore_watering/raw/master/docs/media/valve.mp4">
    Sorry, your browser doesn't support embedded videos, 
    but don't worry, you can
    <a href="https://github.com/kr-g/mpymodcore_watering/raw/master/docs/media/valve.mp4"
    target="_blank">download it</a>
    and watch it with your favorite video player!
  </video>


## Prototype PCB:
 
### Pic A:
  
  Relay board 5V, and 12V jack for Magnetic Valves. 
  5/12V circuts are completely seperated. Powered by 5V/800mA USB, and 12V/1A (both DC) power supply.
  DONT power ESP32 board with USB, and additional supply in parallel. It will DESTROY the board!!!
  
  <img height="640"
      src="https://github.com/kr-g/mpymodcore_watering/raw/master/docs/media/pcb_a.jpg"
    />
  
### Pic B:
  
  <img width="640"
      src="https://github.com/kr-g/mpymodcore_watering/raw/master/docs/media/pcb_b.jpg"
    />


## Prototype in IP Box:
  
  <img height="640"
      src="https://github.com/kr-g/mpymodcore_watering/raw/master/docs/media/ip_boxed.jpg"
    />


## Valves with plumbing wall mounted:
  
  <img height="640"
      src="https://github.com/kr-g/mpymodcore_watering/raw/master/docs/media/valves_wall_mount.jpg"
    />


## Flow meter sensor:

  To track the water amount a flow-meter sensor is used. Inside there is a small rotor and a Hall sensor.
  3 wire with 5V, GND, and signal (use resistor 2k2 pulled to 5V). Signal is just HIGH/LOW every time
  the rotor turns.

### Sensor:

  <img width="640"
      src="https://github.com/kr-g/mpymodcore_watering/raw/master/docs/media/flow_meter.jpg"
    />

### Sensor detail:

  <img width="640"
      src="https://github.com/kr-g/mpymodcore_watering/raw/master/docs/media/flow_meter_detail.jpg"
    />

### Sensor mounted:

  <img width="640"
      src="https://github.com/kr-g/mpymodcore_watering/raw/master/docs/media/flow_meter_mounted.jpg"
    />


## Legal:

  &copy; 2020 k.r.goger - 
  <a href="https://github.com/kr-g/mpymodcore_watering">Project Homepage</a> - 
  <a href="https://github.com/kr-g/mpymodcore_watering/blob/master/LICENSE">License</a>



## Disclaimer

This page is hosted on 
[GitHub Pages](https://pages.github.com/) -
for Data Protection refer to [Privacy information](https://help.github.com/en/articles/github-privacy-statement)
  
 
