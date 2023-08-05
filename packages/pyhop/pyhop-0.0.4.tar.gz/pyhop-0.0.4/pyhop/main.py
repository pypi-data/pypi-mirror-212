import subprocess
import platform


def linux_output(process):
    print("Linux output")
    hop_count = 1
    while True:
        output = process.stdout.readline()
        if not output:
            break
        line = output.decode('utf-8').rstrip()

        if line[0] != 't':
            hop_parts = line.split()
            hop_ip = hop_parts[2].strip("()")
            if hop_ip != '*':
                print(f"{hop_count:2d}  {hop_ip}")
                hop_count += 1


def read_output(process):
    hop_count = 1

    while True:
        output = process.stdout.readline()
        if not output:
            break
        line = output.decode('utf-8').rstrip()
        if line.startswith(" "):
            hop_parts = line.split()
            hop_ip = hop_parts[-1].strip("[]")

            if not any(c.isalpha() for c in hop_ip):
                print(f"hop {hop_count}: {hop_ip}")
                hop_count += 1


def traceroute(hostname):
    system = platform.system()

    if system == 'Windows':
        command = ['tracert', hostname]
        process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        read_output(process)

    elif system == 'Linux':
        # Check if traceroute is installed
        try:
            subprocess.run(['which', 'traceroute'], check=True,
                           stdout=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            print("traceroute is not installed. Try sudo apt install traceroute")
            return

        command = ['traceroute', hostname]
        process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        linux_output(process)
    else:
        print("Unsupported operating system.")
        return

    # Wait for the command to complete
    process.wait()


# Allow running as a standalone script
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Please provide a domain.")
        sys.exit()

    hostname = sys.argv[1]
    traceroute(hostname)
