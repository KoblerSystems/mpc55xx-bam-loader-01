mpc55xx-bam-loader-01
=====================

Upload applications from host to  target with MPC55xx or MPC56xx CPU with the BAM protocol

<pre>
pyhton3 src/mpc55xx/mpc55xx_bam_01.py
</pre>

<pre>
usage: mpc55xx_bam_01.py [-h] [--test {echo,asm} | --image IMAGE]
                         [--address ADDRESS] [--port PORT] [--listen]
                         [--listen_baudrate LISTEN_BAUDRATE] [--sync]
                         [--start_baudrate START_BAUDRATE] [--debug]
                         [--debugWrite] [--debugRead] [--password PASSWORD]
                         [--sendwait SENDWAIT]

optional arguments:
  -h, --help            show this help message and exit
  --test {echo,asm}     some preconfigured tests
  --image IMAGE         download binary image
  --address ADDRESS     load address, hex value, no leading 0x
  --port PORT           serial port
  --listen              listen to serial port AFTER uploading
  --listen_baudrate LISTEN_BAUDRATE
                        listen to serial port AFTER uploading with this
                        baudrate, e.g. 115200
  --sync                MPC56xx only: send sync byte at the beginning for Baud
                        Rate Detection
  --start_baudrate START_BAUDRATE
                        MPC56xx: start with baudrate, MPC55xx: only 9600
  --debug               provide debug output
  --debugWrite          provide debug output for write to target serial port
  --debugRead           provide debug output for read from target serial port
  --password PASSWORD   Password: 8byte, hex, spaces allowed, e.g. FEED FACE
                        CAFE BEEF
  --sendwait SENDWAIT   Time to wait before sending a byte, in seconds, may be
                        float number
</pre>
