import os
import subprocess
import speedtest
from datetime import datetime

# Get up paths for 3rd party applications
script_dir = os.path.dirname(os.path.realpath(__file__))
fast_app_path = os.path.join(script_dir, 'apps', 'fast_windows_amd64.exe')
speedtest_app_path = os.path.join(script_dir, 'apps', 'speedtest.exe')
powershell_app_path = 'C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe'
ookla_speedtest_app_path = os.path.join(script_dir, 'apps', 'ookla-speedtest.exe')

def run_fast():
	print("Starting Fast")
	fast_proc = subprocess.Popen(fast_app_path, shell=False, stdout=subprocess.PIPE)
	fast_results = str(fast_proc.stdout.readline())
	fast_result = fast_results.rsplit('->')[1].rstrip('\\n\'').strip(' ')
	print(fast_result)
	return fast_result

def run_speedtest():
	print("Starting speedtest-cli")
	s = speedtest.Speedtest()
	s.get_best_server()
	s.download(threads=1000)
	results = s.results.dict()
	#print(results)
	speedtest_result = str(round(results['download'] / 1048576, 2)) + ' Mbps'
	print(speedtest_result)
	return speedtest_result

def run_powershell(url):
	print("Starting Powershell Download")
	powershell_proc = subprocess.Popen([powershell_app_path, '-f', os.path.join(script_dir, url)], shell=False, stdout=subprocess.PIPE)
	powershell_results = str(powershell_proc.stdout.readline())
	powershell_result = powershell_results.split(' ')[0].strip('b\'') + ' Mbps'
	print(powershell_result)
	return powershell_result

def run_ookla_speedtest():
	print("Starting Ookla Speedtest")
	ookla_proc = subprocess.Popen([ookla_speedtest_app_path, '-f', 'csv', '-p', 'no'], shell=False, stdout=subprocess.PIPE)
	ookla_results = str(ookla_proc.stdout.readline())
	ookla_result = str(round(int(ookla_results.split(',')[6].strip('"').rstrip('"')) / 125000, 2)) + ' Mbps'
	print(ookla_result)
	return ookla_result

# Get the current timestamp and format it so that we know what time our results are from.
now = datetime.now()
dt_string = now.strftime("%Y/%m/%d %H:%M:%S")

# Run the various applications and get their results back.
# Returned results should already be converted to Mbps.
fast = str(run_fast())
speedtest = str(run_speedtest())
turnkey = str(run_powershell("turnkey.ps1"))
ookla = str(run_ookla_speedtest())

# Append results to our report.csv file.
with open(os.path.join(script_dir, 'report.csv'), 'a+') as file_out:
	file_out.write(dt_string + ',' + fast + ',' + speedtest + ',' + turnkey + ',' + ookla + '\n')
