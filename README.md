mpc55xx-bam-loader-01
=====================

Upload applications from host to  target with MPC55xx or MPC56xx CPU with the BAM protocol

<pre>
pyhton3 src/mpc55xx/mpc55xx_bam_01.py
</pre>

<pre>
usage: mpc55xx_bam_01.py [-h] [--test {echo,asm} | --image IMAGE]
                         [--address ADDRESS] [--port PORT] [--listen] [--sync]
                         [--debug] [--password PASSWORD] [--sendwait SENDWAIT]

optional arguments:
  -h, --help           show this help message and exit
  --test {echo,asm}    some preconfigured tests
  --image IMAGE        download binary image
  --address ADDRESS    load address, hex value, no leading 0x
  --port PORT          serial port
  --listen             listen to serial port AFTER uploading, speed 115200
  --sync               MPC56xx only: send sync byte at the beginning for Baud
                       Rate Detection
  --debug              provide debug output
  --password PASSWORD  Password: 8byte, hex, spaces allowed, e.g. FEED FACE
                       CAFE BEEF
  --sendwait SENDWAIT  Time to wait before sending a byte, in seconds, may be
                       float number
</pre>
