## Signal Calibration
Please refer to the instructions in `documentation/`

1. run `. setup.sh` to source the correct python path
2. keep all classes needed in `python/`, scripts belong into `share/`. Documentation is in `documentation/`, data in `data/`

### Instructions:
Please refer to documentation/ which contains extensive step-by-step instructions.

#### fun with ports:
List available ports: `ls /dev/tty*`

The arduino normally appears as one of the USB ports (e.g. `/dev/ttyUSB0`), the signal generator as a ACM port (e.g. `/dev/ttyACM0`) [why?](https://rfc1149.net/blog/2013/03/05/what-is-the-difference-between-devttyusbx-and-devttyacmx/ "Blog post explanation of the difference...")

To give the user the permission to access a port:
`sudo chmod 666 <portname>`

Note that this only gives the access within the terminal in which the command has been run.
  
#### project structure:
keep all classes needed in `python/`, scripts belong into `share/`. Documentation is in `documentation/`, data in `data/`
Dont forget to source `setup.sh`!
