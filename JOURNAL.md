---
title: "FTDI Board"
author: pn2222a
descrriptioni: "FTDI USB board based on FT232RL chip"
created_at: "2026-06-21T02:59:14Z"
---



# June 10: project start and component selection

started the project. needed a usb-to-uart board for flashing esp32 and other mcus, got tired of borrowing from the lab. the lab ones are always either broken or being used by someone else anyway.

spent a while on the ic. ft232rl is old but its cheap and everyone has docs on it. looked at cp2102 too but the ft232rl has more cbus pins and full flow control so it wins for debugging. probably should have checked if its end of life yet but whatever, its everywhere so itll be fine.

picked tlv75733 for 3.3v, switchable to 5v for the output. usblc6 for esd on the data lines. pptc fuse on the input because im clumsy and i dont want to fry a laptop usb port. usb-c because its 2026 obviously.

wrote out the whole passive list too - 25x 10k, 4x 1k, a 100k, 2x 5.1k, 2x 33r, and the caps. all 0805. made the kicad project skeleton.

![sch power](images/SCH1.png)

**Total time spent: 2 hours**

# June 11: schematic - power section

did the power section first.

usb-c with two 5.1k cc pulldowns so it acts as a device. took forever to get the orientation and cc1/cc2 wiring right, and figuring out which pins to tie for usb2.0. kept second guessing whether i needed the shield connected to gnd or through a resistor.

esd protection with usblc6 between d+/d- and gnd. 33r series on each data line, sized the caps so the impedance stays in usb2.0 range. the differential impedance math took me a few tries but i think ive got it close enough, usb2.0 is forgiving.

pptc on vbus with a 100nf right at the connector. ldo with 10uf in and out, plus a 4.7uf further down the rail. the slide switch picks between 3.3v and 5v.

tricky bit was making sure the switch cant back-feed the regulator and short vbus to gnd. ended up putting the mosfet in the load path to stop that. not sure if its overkill but its cheap and it works.

![sch power](images/SCH1.png)

**Total time spent: 3 hours**

# June 13: schematic - ft232rl core

added the ft232rl.

crystal-less, it has an internal clock, saved a bunch of space and a couple of parts. checked the osc settings work at both 3.3v and 5v. honestly glad i dont have to mess with crystal load caps, those always trip me up.

decoupling caps on every power pin, right values on the internal reg output. went through the datasheet pin by pin so nothing floats - pulled the unused ones to a known state. the datasheet pdf is ancient but at least its thorough.

hooked the status pins (txd rxd rts cts dtr dsr dcd ri) to the led network.

then the esp auto-reset circuit with the two bc817s on dtr/rts. this was the worst part. the ide toggles dtr/rts to enter bootloader and the transistors have to pull esp enable and gpio0 at the right times. spent ages getting the polarity right so the reset sequence matches what esptool wants, 100k pullup on reset so it sits high by default. i read like three different forum posts about this before it clicked.

![sch core](images/SCH2.png)

**Total time spent: 4 hours**

# June 14: schematic - leds and connectors

finished the leds. 12 of them. 2 green for power, yellow for tx, blue for rx, 2 orange for flow control, red for dtr, 5 white for cbus. probably way more than i need but i like seeing what the chip is doing at a glance.

each one gets a 1k series resistor so they run at like 2-3ma. had to redo the values per color since red/blue/green/yellow/white all have different forward voltages. the blues and whites are annoyingly bright even at low current so i might dial those back later.

added the headers - 1x7 for uart, 1x4 for extra cbus/gpio. everything 0805 so i can hand solder it. i hate soldering anything smaller than 0805, did enough of that in the lab already.

also put in two uln2003s to buffer the cbus outputs, open-collector so i can switch bigger stuff than leds later. honestly not sure i need them but theyre cheap insurance.

did the full review at the end, ran erc. caught two nets that were the same signal with different names and a polarity error on a transistor. fixed em, erc is clean now. saved a real headache down the line with those net names, board house would have probably rejected it.

![sch leds](images/SCH3.png)

**Total time spent: 3 hours**

# June 16: initial pcb layout

imported the netlist and started placing.

usb connector on one edge, headers on the opposite so it sits nice on a breadboard. ft232rl in the middle with bypass caps shoved right against its power pins. i kept the caps within a couple mm of the pins, that whole "0.1uf as close as possible" thing is real.

led resistors next to their leds to keep the fan-out clean. power stuff (ldo switch mosfet) in a corner so the switching noise stays away from usb. also rotated the silkscreens around so the labels wouldnt be upside down, small thing but it bugs me.

75x50mm with m3 holes in the corners, fits a case. went 4-layer - signal/gnd/power/signal - makes routing way easier. costs a bit more per board but whatever, this is a one off.

moved components around a lot until the ratsnest crossings were low and the usb path to the ft232rl was short. placement is everything, bad placement ruins the routing later.

![pcb placement](images/SCH4.png)

**Total time spent: 4 hours**

# June 17: pcb routing

started routing. 0.5mm power traces, 0.2mm signals, 0.2mm clearance. probably fine for the currents here, the leds barely draw anything.

inner layers are the gnd and 3.3v planes so the outer layers stay free for signals. this is why 4-layer is nice, i barely had to think about return paths, there's a plane under everything. no ground loops to worry about on a board this small anyway.

did the usb differential pair first since its the critical one. kept d+/d- together and length matched, series resistors inline, no vias in the pair. matched them to within like a mm which is way better than usb2.0 needs.

set up the planes with thermal reliefs so soldering isnt a nightmare of heat sinking. first board i forgot those and the whole plane was a heatsink, never again.

then fanned the ft232rl out - status pins to their leds and resistors, power rails to the planes.

![pcb routing](images/SCH5.png)

**Total time spent: 5 hours**

# June 18: pcb routing continued

finished the rest - auto-reset circuit, cbus buffering, header connections. the auto-reset transistors got shoved in a corner with their resistors which is a bit cramped but it fits.

got all the leds routed through their resistors as a clean fan-out from the status pins. tried to keep the led traces grouped by color so the board looks organized.

thermal reliefs on the plane connections, 33r usb resistors as close to the connector as i could get them.

drc flagged a few clearance violations near the usb connector where the cc resistors and esd were fighting for space. fixed those, and some ugly via fanout angles. widened a couple power traces after adding up the led current, 0.5mm was honestly fine but 0.7mm feels safer.

cleaned up the rest - killed unnecessary vias, straightened traces so it doesnt look like spaghetti. this always takes longer than i expect, its the fiddly part of routing.

![pcb routing2](images/SCH6.png)

**Total time spent: 4 hours**

# June 19: final pcb touches

silkscreen labels on everything. connectors, switch positions (3.3v/5v), led polarity, reference designators where you can actually read them. left enough space around the labels so they dont get wiped out by the mask.

project name and version on the board, small maker mark.

added a moon on the silkscreen as an easter egg. took a while to get the graphic converted so it wouldnt overlap pads or courtyards. traced it in inkscape first because i couldnt find a good image to import.

final drc across everything - clearance, silkscreen to pad, courtyard overlaps, unconnected nets. all passed. honestly thought thered be something but it was clean first try.

exported gerbers and checked em in the previewer so nothing was flipped or missing. drill file looks right too.

![pcb final](images/SCH7.png)

**Total time spent: 3 hours**

# June 20: finished board

finished the board.

added more easter eggs - a tiny rocket next to the moon, and a smiley on the back. probably only me that ever uses this but the details make it fun. noticed the smiley and the rocket kind of tell a story which is neat.

checked the ft232rl footprint against the datasheet pin spacing again, usb connector pins line up, mounting holes clear everything. printed it out at 1:1 on paper just to eyeball the component sizes and make sure nothing felt impossibly small.

exported the final fab files - gerbers, drills, pick and place. last look in the 3d viewer. went back and forth on the solder mask color for like an hour before ordering, ended up purple.

![pcb](images/PCB.png)

**Total time spent: 6 hours**

# June 21: polishing repo
adding images from kicad and will start blendering soon for some cool renders
i need to learn how to make the renders faster.
spent a bunch of the time just exporting screenshots from kicad and cropping them so they dont look terrible in the readme.
![sch](images/SCH1.png)

**Total time spent: 2 hours**

# June 23: Blender
started blender model for pcb
red solder mask, white silkscreen, enig finish
set up a few test renders to get the lighting right, the board keeps coming out too dark or too shiny, still fiddling with it
![render](images/blender-viewport1.png)

**Total time spent: 3 hours**

# June 24: polish readme
adding images to readme and make bom.csv draft for parts and whatnot
will make more blender renders soon with animations and effects
also played around with a turntable animation idea for the board, not sure if i'll commit to it yet
![sch](images/SCH2.png)

**Total time spent: 3 hours**

# June 25: BOM
looked for parts and made a bom
parts are from lcsc
added pcbs from jlcpcb and pcbway just in case
the more the merrier they say
took a while going through every single resistor and cap to find the right lcsc part number, stock kept running out on the cheap ones
![sch](images/SCH3.png)

**Total time spent: 4 hours**
