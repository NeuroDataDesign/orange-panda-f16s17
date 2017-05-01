# written by eric bridgeford
import psutil
import time
import argparse

def cpulog(outfile):
    with open(outfile, 'w') as outf:
        while(True):
            cores = psutil.cpu_percent(percpu=True)
            corestr = ",".join([str(core) for core in cores])
            outf.write(corestr + '\n')
            outf.flush()
            time.sleep(1)  # delay for 1 second

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('outfile', help='the file to write core usage to.')
    args = parser.parse_args()
    cpulog(args.outfile)

if __name__ == "__main__":
    main()
