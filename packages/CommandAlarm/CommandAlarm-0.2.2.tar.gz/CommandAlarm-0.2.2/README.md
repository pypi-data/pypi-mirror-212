# CommandAlarm

CommandAlarm is a simple command line program that allows users to set an alarm with a custom command. 

## Installation

To install CommandAlarm, you can use [pip](https://pip.pypa.io/en/stable/):

```bash
pip install commandalarm
```

Alternatively, you can clone the repository and install it manually:

```bash
git clone https://github.com/alofgren/commandalarm.git
cd commandalarm
pip install .
```

## Usage Output

```bash
usage: commandalarm [-h] [-v] [-d {1,2,3,4,5,6,7}] [-r] [-s] [-n] [-t TIMEOUT] time command [command ...]

Set an alarm with a custom command.

positional arguments:
  time                  the time in the format HH:MM:SS
  command               the command to run

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -d {1,2,3,4,5,6,7}, --day {1,2,3,4,5,6,7}
                        the day of the week as an integer from 1 to 7, where 1 represents Monday
  -r, --repeat          repeat indefinitely
  -s, --shell           run command with shell
  -n, --no-check        don't check the command return code
  -t TIMEOUT, --timeout TIMEOUT
                        timeout in seconds for the command to complete
```

## Examples

To set an alarm for 2:00 PM on Tuesday, and play a sound when the alarm goes off:
```bash
commandalarm -d 2 14:00:00 aplay alarm_sound.wav
```

To set an alarm for 10:00 PM to run a command with shell and repeat indefinitely: 
```bash
commandalarm 22:00:00 -r -s 'echo "Hello, world!"'
```

To set an alarm for 9:15 AM on Wednesday to run a Python script with a timeout of 30 seconds: 
```bash
commandalarm 09:15:00 -d 3 -t 30 python3 script.py
```

## Contributing

If you would like to contribute to CommandAlarm, please feel free to submit a pull request or open an issue on the [GitHub repository](https://github.com/alofgren/commandalarm).

## Donate

If you find this program useful, please consider making a donation.

**Bitcoin (BTC):** bc1qdnnfjl7k9xrsl2fydrffxpg7e4mm5f57p9qwgg

**Ethereum (ETH):** 0x2B29d1A7d94501b6491a26DF54550b0AF793235F

**Litecoin (LTC):** ltc1qhvyfnayhwk3udakyynppc2uy2y2fv97lnt8y7w

## License

CommandAlarm is licensed under the [GPL License](https://github.com/alofgren/commandalarm/blob/master/LICENSE).
