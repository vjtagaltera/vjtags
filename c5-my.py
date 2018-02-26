#!/usr/bin/python

#
# A general test and demonstration of several urjtag operations from python.
#

# works in both python 2 and 3
def printf(format, *args):
     """Format args with the first argument as format string, and print.
     If the format is not a string, it is converted to one with str.
     You must use printf('%s', x) instead of printf(x) if x might
     contain % or backslash characters."""
     sys.stdout.write(str(format) % args)

import sys
sys.path.append( "." )

import urjtag

urjtag.loglevel(urjtag.URJ_LOG_LEVEL_WARNING)

urc = urjtag.chain()
printf("%s\n", urc);

urc.cable("usbblaster", "driver=ftdi")
printf("urc.cable done %s\n", urc)

urc.test_cable()
printf("urc.test_cable done\n")

f = urc.get_frequency()
printf("frequency was %d Hz\n", f)

urc.reset();

urc.tap_detect()
printf("urc.detect done\n")
printf("chainlength=%d\n", urc.len())

printf("id[0]=%08x\n", urc.partid(0) );

urc.run_svf("DE0_Comm.svf")

urc.reset()
urc.tap_detect()
urc.reset()

### Main code
urc.set_instruction("SAMPLE/PRELOAD")
urc.shift_ir()
drval = urc.get_dr_in()
printf("BSR dr_in result: %s\n", drval)
urc.shift_dr()
drval = urc.get_dr_out_string()
printf("BSR dr_out result: %s\n", drval)

urc.set_instruction("IDCODE")
urc.shift_ir()
urc.shift_dr()
drval = urc.get_dr_out()
printf("IDREG dr result: %08X\n", drval)

urc.set_instruction("USERCODE")
urc.shift_ir()
urc.shift_dr()
drval = urc.get_dr_out()
printf("USERCODEREG dr result: %08X\n", drval)

# Set up our new Virtual UART instructions
urc.add_register("SIR", 5)
urc.add_register("SDR", 8)
urc.add_instruction("SIR","0000001110","SIR")
urc.add_instruction("SDR","0000001100","SDR")

urc.set_instruction("SIR")
urc.shift_ir()
urc.set_dr_in(0x12)
urc.shift_dr()
urc.set_instruction("SDR")
urc.shift_ir()
urc.shift_dr()
printf("Status: %s\n", urc.get_dr_out_string() )

urc.set_instruction("SIR")
urc.shift_ir()
urc.set_dr_in(0x10)
urc.shift_dr()
urc.set_instruction("SDR")
urc.shift_ir()
urc.set_dr_in(0)
for cntr in range(1,65):
	urc.shift_dr()
	drval = urc.get_dr_out()
	printf("%c", drval)

printf("\nDone!\n");

urc.set_instruction("SIR")
urc.shift_ir()
urc.set_dr_in(0x11) ### Write register
urc.shift_dr()
urc.set_instruction("SDR")
urc.shift_ir()
urc.set_dr_in(65)
urc.shift_dr()
urc.set_dr_in(66)
urc.shift_dr()


urc.set_instruction("SIR")
urc.shift_ir()
urc.set_dr_in(0x10)
urc.shift_dr()
urc.set_instruction("SDR")
urc.shift_ir()
urc.set_dr_in(0)
urc.shift_dr()
drval = urc.get_dr_out()
printf("%c\n", drval)
urc.shift_dr()
drval = urc.get_dr_out()
printf("%c\n", drval)


urc.set_instruction("SIR")
urc.shift_ir()
urc.set_dr_in(0x12)
urc.shift_dr()
urc.set_instruction("SDR")
urc.shift_ir()
urc.shift_dr()
printf("Status: %s\n", urc.get_dr_out_string() )

urc.set_instruction("BYPASS")
urc.shift_ir()
