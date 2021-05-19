## Signal Calibration
1. run `. setup.sh`\\
2. run scripts in `share`, keep data in `data`\\

#### fun with ports:
list available ports: `ls /dev/tty*`\\
the arduino normally appears as one of the USB ports (e.g. `/dev/ttyUSB0`), the signal generator as a ACM port (e.g. `/dev/ttyACM0`) [why?](https://rfc1149.net/blog/2013/03/05/what-is-the-difference-between-devttyusbx-and-devttyacmx/ "Blog post explanation of the difference...")\\
Give the user the permission to access a port:
`sudo chmod 666 <portname>`
####project structure:
keep all classes needed in `python`, scripts belong into `share`.
Dont forget to source `setup.sh`!
