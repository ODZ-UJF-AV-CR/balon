#!/usr/bin/python

import subprocess
import logging
import shlex
import fcntl
import select
import sys
import os


def start_process(child):
	logging.info('launching %s' % child['name'])
	child['popen'] = subprocess.Popen(shlex.split(child['cli']),
									  stdout=child['stdout'],
									  stderr=subprocess.PIPE)
	child['active'] = True
	child['stderr_residue'] = ''

	fileno = child['popen'].stderr.fileno()
	flag = fcntl.fcntl(fileno, fcntl.F_GETFL)
	fcntl.fcntl(fileno, fcntl.F_SETFL, flag | os.O_NONBLOCK)


children = [
	{
		'name': "monitor",
		'cli': "python /home/odroid/git/balon/scripts/monitor_p.py",
		'on_exit': start_process,
		'stdout': open('/dev/zero')
	},
	{
		'name': "m_koule",
		'cli': "python /home/odroid/git/balon/fik2/m_koule.py",
#		'on_exit': lambda: children[0].terminate(),
		'stdout': open('/dev/zero')
	},
	{
		'name': 'vlc_file',
		'cli': "/home/odroid/git/balon/fik2/vlc_file.sh",
		'stdout': open('/dev/zero')
	}
]


def main():
	for child in children:
		start_process(child)

	while True:
		stderr_fds = [child['popen'].stderr for child in children if child['active']]

		if not stderr_fds:
			logging.info('exiting')
			sys.exit(1)

		ready_fds, _wr, _xr = select.select(stderr_fds, [], [], 1000)

		for fd in ready_fds:
			child = ([ch for ch in children if ch['popen'].stderr == fd] \
					or [{'name': 'unknown process'}])[0]
			process_name = child['name']

			try:
				split = (child.get('stderr_residue', '') + fd.read()).split('\n')
				child['stderr_residue'] = split.pop()

				for line in split:
					sys.stderr.write("[%s] %s\n" % (process_name, line))
			except Exception as e:
				if not child['popen'].poll():
					logging.warning('%s: read from pipe exception: %s' % (process_name, e))

		for child in children:
			if child['active'] and child['popen'].poll() is not None:
				logging.warning('%s exited with code %d' % (process_name, \
															child['popen'].returncode))
				child['active'] = False
				child.get('on_exit', lambda a: None)(child)


if __name__ == "__main__":
	main()

