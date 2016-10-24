#!/usr/bin/env python

"""Simple HTTP Server With Upload.

This module builds on BaseHTTPServer by implementing the standard GET
and HEAD requests in a fairly straightforward manner.

"""


import os, sys
lib_path = os.path.abspath(os.path.join('..', 'pipeline', 'src'))
sys.path.append(lib_path)


import posixpath
import BaseHTTPServer
import urllib
import cgi
import shutil
import mimetypes
import re

from utils.get_data import get_record, get_patients, make_h5py_object
from utils.clean_data import get_eeg_data, get_times, get_electrode_coords
from utils.fourier import butter_highpass_filter, butter_lowpass_filter, butter_bandstop_filter
from preprocessing.interp import fit_sphere, gc, gc_invdist_interp
from main import set_args, clean, detect_bad_channels, interpolate, reduce_noise 
from markdown import markdown
import matplotlib.pyplot as plt
from utils.plots import (plot_timeseries,
                         make_3d_scatter,
                         make_spectrogram,
                         my_save_fig)
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import ast
import h5py
import pypandoc
import zipfile
import shutil

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO


class SimpleHTTPRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    """Simple HTTP request handler with GET/HEAD/POST commands.

    This serves files from the current directory and any of its
    subdirectories.  The MIME type for files is determined by
    calling the .guess_type() method. And can reveive file uploaded
    by client.

    The GET/HEAD/POST requests are identical except that the HEAD
    request omits the actual contents of the file.

    """

    def do_analysis(self, fn):
        #!! REMOVE
        out = ''

        # Figure out which patient this is
        patient = os.path.basename(fn)
        out = "# Upload Report for File at " + str(patient) + ".\n"

        # Create folder for results if doesn't exist
        # Also set path variables to save data to later
	res_path = "results/" + patient + '/'
	img_path = "results/" + patient + "/imgs/"
	img_rel = "imgs/"
	if not os.path.exists(res_path):
	    os.makedirs(res_path)
	if not os.path.exists(img_path):
	    os.makedirs(img_path)

        # Get pipeline parameters from 'pipeline.conf'
        set_args()

        # Load data from file path
        d = make_h5py_object(fn)

        # Wrap this patient's data.
        # Our functions take an array of patients,
        # but we are only doing one patient here.
        D = [d]

        # Clean the data
        clean_data, clean_report = clean(D)
        out += clean_report
        eeg_data, times, coords = clean_data
        from utils.clean_data import get_electrode_coords
        cart = get_electrode_coords(D[0], coords = "euclidian")

        # We only have one patient for this example
	d = eeg_data[:, :, -1]
	t = times[:, :, -1]

        # Make and add the brain scatter plot to report
        out += my_save_fig(make_3d_scatter(d, cart),
                img_path + "3d_brain.png",
                "Example 3D Scatter Plot")

        scat = plot_timeseries(data = d,
            time = t,
            selector = "random",
            title = "10 randomly selected electrodes from data.",
            start = 1500,
            end = 2000,
            skip = 1,
            randno = 10,
            xlab = r'$t$, in milliseconds',
            ylab = r'voltage in $mV$')

        out += my_save_fig(scat, img_path + "rand_time_series.png",
                    "Randomly Selected Electrode Time Series")
        # Detect bad electrodes, plot them.
        bad_chans, bad_report = detect_bad_channels(eeg_data)
        out += bad_report
        bad_plot = plot_timeseries(data = d[:, bad_chans[0]],
            time = t,
            selector = "all",
            title = "Plot of the bad electrodes.",
            start = 1000,
            end = 2000,
            skip = 1,
            randno = 10,
            xlab = r'$t$, in milliseconds',
            ylab = r'voltage in $mV$')

        # Plot the bad channels
        out += my_save_fig(bad_plot, img_path + "bad_electrodes.png",
                    "The 'Bad' Electrodes")

        # Interpolate bad electrodes
        pool = 10 # How many electrodes to interp against?
        int_data, int_report = interpolate(eeg_data, coords,
				bad_chans, npts = pool)
        eeg_data, closest = int_data
        out += int_report

        # Plotting the interpolated electrodes
	for l in range(len(closest[0])):
	    out += "\nInterpolating for channel: " + \
			str(bad_chans[0][l]) + '\n'
	    out +=  "\nInterpolating against: " + str(closest[0][l]) + '\n'
	    inds = closest[0][l]
	    d = np.column_stack([eeg_data[:, i, 0] for i in inds])
	    d = np.column_stack([d, eeg_data[:, bad_chans[0][l], 0]])
	    cols = ["red"] * pool
	    cols.append("blue")
	    tmp_fig = plot_timeseries(data = d,
			  time = t,
			  selector = "all",
			  title = "Interpolated (blue) electrode with " + \
			    " its " + str(pool) + " closest neighbors.",
			  colors = cols,
			  start = 100,
			  end = 2000,
			  skip = 10,
			  xlab = r'$t$, in milliseconds',
			  ylab = r'difference from mean' + \
				    'voltage in $mV$')
            title = "Interpolation of Electrode " + str(l)
            out += my_save_fig(tmp_fig, img_path + "elect_interp_" + \
                            str(l) + ".png", title)


        # Reduce noise on data
        eeg_data_filtered = reduce_noise(eeg_data)

        # Plot spectrograms (before and after) for each channel
	for i in range(5):#eeg_data.shape[1]):
            fig = plt.figure()
            fig.suptitle("Channel " + str(i), fontsize=10)
            plt.subplot(211)	
            make_spectrogram(eeg_data[:, i, 0], fig)
            plt.subplot(212)	
            make_spectrogram(eeg_data_filtered[:, i, 0], fig)
	    plt.tight_layout()
	    plt.savefig(img_path + "spectrogram_channel_"+str(i)+".png")
            plt.clf()
            plt.close(fig)

        # Plot example spectrogram for the report
	out += "## Here is a sample of channel 4 before and after noise reduction.\n"
	out +=  '![](' + img_path + 'spectrogram_channel_4.png ' + \
			'\"sp Image\")\n'

        # Saving everything
#	np.savetxt(res_path + "pre_processed.csv", eeg_data_filtered,
#			delimiter=",")
        html_text = markdown(out, output_format='html5')
	report = pypandoc.convert(html_text, 'pdf', format = "html",
		outputfile=res_path + "out.pdf")	
	ziph = zipfile.ZipFile("results/" + patient + '.zip', 'w', zipfile.ZIP_DEFLATED)
	for root, dirs, files in os.walk(res_path):
	    for file in files:
		print "zipping", root, file
		ziph.write(os.path.join(root, file))
	ziph.close()
	#os.remove(res_path + "pre_processed.csv")
	return html_text, "results/" + patient + ".zip"


    def do_GET(self):
        """Serve a GET request."""
        f = self.send_head()
        if f:
            self.copyfile(f, self.wfile)
            f.close()

    def do_HEAD(self):
        """Serve a HEAD request."""
        f = self.send_head()
        if f:
            f.close()

    def do_POST(self):
        """Serve a POST request."""
        r, info, res, link = self.deal_post_data()
        print r, info, "by: ", self.client_address
        f = StringIO()
        f.write('<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">')
        f.write("<html>\n<title>Upload Result Page</title>\n")
        f.write("<body>\n<h2>Upload Result Page</h2>\n")
        f.write("<hr>\n")
        if r:
            f.write("<strong>Success:</strong>")
            f.write("<a href=\"%s\">Download the full analyzis .zip</a>" % link)
        else:
            f.write("<strong>Failed:</strong>")
        f.write("<br><strong>Analysis for this file is below. </strong>")
        f.write(res)
        f.write("<br><a href=\"%s\">back</a>" % self.headers['referer'])
	f.write
        f.write("</body>\n</html>\n")
        length = f.tell()
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-Length", str(length))
        self.end_headers()
        if f:
            self.copyfile(f, self.wfile)
            f.close()
        
    def deal_post_data(self):
        boundary = self.headers.plisttext.split("=")[1]
        remainbytes = int(self.headers['content-length'])
        line = self.rfile.readline()
        remainbytes -= len(line)
        if not boundary in line:
            return (False, "Content NOT begin with boundary")
        line = self.rfile.readline()
        remainbytes -= len(line)
        fn = re.findall(r'Content-Disposition.*name="file"; filename="(.*)"', line)
        if not fn:
            return (False, "Can't find out file name...")
        path = self.translate_path(self.path)
        fn = os.path.join(path, 'files', fn[0])
        print fn
        line = self.rfile.readline()
        remainbytes -= len(line)
        line = self.rfile.readline()
        remainbytes -= len(line)
        try:
            out = open(fn, 'wb')
        except IOError:
            return (False, "Can't create file to write, do you have permission to write?")
                
        preline = self.rfile.readline()
        remainbytes -= len(preline)
        while remainbytes > 0:
            line = self.rfile.readline()
            remainbytes -= len(line)
            if boundary in line:
                preline = preline[0:-1]
                if preline.endswith('\r'):
                    preline = preline[0:-1]
                out.write(preline)
                out.close()
                res, link = self.do_analysis(fn)
                return (True, "File '%s' upload success!" % fn, res, link)
            else:
                out.write(preline)
                preline = line
        return (False, "Unexpect Ends of data.")

    def send_head(self):
        """Common code for GET and HEAD commands.

        This sends the response code and MIME headers.

        Return value is either a file object (which has to be copied
        to the outputfile by the caller unless the command was HEAD,
        and must be closed by the caller under all circumstances), or
        None, in which case the caller has nothing further to do.

        """
        path = self.translate_path(self.path)
        f = None
        if os.path.isdir(path):
            if not self.path.endswith('/'):
                # redirect browser - doing basically what apache does
                self.send_response(301)
                self.send_header("Location", self.path + "/")
                self.end_headers()
                return None
            for index in "index.html", "index.htm":
                index = os.path.join(path, index)
                if os.path.exists(index):
                    path = index
                    break
            else:
                return self.list_directory(path)
        ctype = self.guess_type(path)
        try:
            # Always read in binary mode. Opening files in text mode may cause
            # newline translations, making the actual size of the content
            # transmitted *less* than the content-length!
            f = open(path, 'rb')
        except IOError:
            self.send_error(404, "File not found")
            return None
        self.send_response(200)
        self.send_header("Content-type", ctype)
        fs = os.fstat(f.fileno())
        self.send_header("Content-Length", str(fs[6]))
        self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
        self.end_headers()
        return f

    def list_directory(self, path):
        """Helper to produce a directory listing (absent index.html).

        Return value is either a file object, or None (indicating an
        error).  In either case, the headers are sent, making the
        interface the same as for send_head().

        """
        try:
            list = os.listdir(path)
        except os.error:
            self.send_error(404, "No permission to list directory")
            return None
        list.sort(key=lambda a: a.lower())
        f = StringIO()
        displaypath = cgi.escape(urllib.unquote(self.path))
        f.write('<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">')
        f.write("<html>\n<title>Directory listing for %s</title>\n" % displaypath)
        f.write("<body>\n<h2>Directory listing for %s</h2>\n" % displaypath)
        f.write("<hr>\n")
        f.write("<form ENCTYPE=\"multipart/form-data\" method=\"post\">")
        f.write("<input name=\"file\" type=\"file\"/>")
        f.write("<input type=\"submit\" value=\"upload\"/></form>\n")
        f.write("<hr>\n<ul>\n")
        for name in list:
            fullname = os.path.join(path, name)
            displayname = linkname = name
            # Append / for directories or @ for symbolic links
            if os.path.isdir(fullname):
                displayname = name + "/"
                linkname = name + "/"
            if os.path.islink(fullname):
                displayname = name + "@"
                # Note: a link to a directory displays with @ and links with /
            f.write('<li><a href="%s">%s</a>\n'
                    % (urllib.quote(linkname), cgi.escape(displayname)))
        f.write("</ul>\n<hr>\n</body>\n</html>\n")
        length = f.tell()
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-Length", str(length))
        self.end_headers()
        return f

    def translate_path(self, path):
        """Translate a /-separated PATH to the local filename syntax.

        Components that mean special things to the local file system
        (e.g. drive or directory names) are ignored.  (XXX They should
        probably be diagnosed.)

        """
        # abandon query parameters
        path = path.split('?',1)[0]
        path = path.split('#',1)[0]
        path = posixpath.normpath(urllib.unquote(path))
        words = path.split('/')
        words = filter(None, words)
        path = os.getcwd()
        for word in words:
            drive, word = os.path.splitdrive(word)
            head, word = os.path.split(word)
            if word in (os.curdir, os.pardir): continue
            path = os.path.join(path, word)
        return path

    def copyfile(self, source, outputfile):
        """Copy all data between two file objects.

        The SOURCE argument is a file object open for reading
        (or anything with a read() method) and the DESTINATION
        argument is a file object open for writing (or
        anything with a write() method).

        The only reason for overriding this would be to change
        the block size or perhaps to replace newlines by CRLF
        -- note however that this the default server uses this
        to copy binary data as well.

        """
        shutil.copyfileobj(source, outputfile)

    def guess_type(self, path):
        """Guess the type of a file.

        Argument is a PATH (a filename).

        Return value is a string of the form type/subtype,
        usable for a MIME Content-type header.

        The default implementation looks the file's extension
        up in the table self.extensions_map, using application/octet-stream
        as a default; however it would be permissible (if
        slow) to look inside the data to make a better guess.

        """

        base, ext = posixpath.splitext(path)
        if ext in self.extensions_map:
            return self.extensions_map[ext]
        ext = ext.lower()
        if ext in self.extensions_map:
            return self.extensions_map[ext]
        else:
            return self.extensions_map['']

    if not mimetypes.inited:
        mimetypes.init() # try to read system mime.types
    extensions_map = mimetypes.types_map.copy()
    extensions_map.update({
        '': 'application/octet-stream', # Default
        '.py': 'text/plain',
        '.c': 'text/plain',
        '.h': 'text/plain',
        })


def test(HandlerClass = SimpleHTTPRequestHandler,
         ServerClass = BaseHTTPServer.HTTPServer):
    BaseHTTPServer.test(HandlerClass, ServerClass)

if __name__ == '__main__':
    test()
