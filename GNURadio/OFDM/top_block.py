#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Top Block
# Generated: Wed Oct  3 17:36:45 2012
##################################################

from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.gr import firdes
from grc_gnuradio import blks2 as grc_blks2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import wx

class top_block(grc_wxgui.top_block_gui):

	def __init__(self):
		grc_wxgui.top_block_gui.__init__(self, title="Top Block")
		_icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
		self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

		##################################################
		# Variables
		##################################################
		self.samp_rate = samp_rate = 10e6

		##################################################
		# Blocks
		##################################################
		self.gr_throttle_0 = gr.throttle(gr.sizeof_gr_complex*1, samp_rate)
		self.gr_file_source_0 = gr.file_source(gr.sizeof_gr_complex*1, "/home/traviscollins/git/BLISS/GNURadio/OFDM/received_p.txt", True)
		self.gr_file_sink_0 = gr.file_sink(gr.sizeof_char*1, "/home/traviscollins/git/BLISS/GNURadio/OFDM/output.txt")
		self.gr_file_sink_0.set_unbuffered(False)
		self.digital_ofdm_demod_0 = grc_blks2.packet_demod_b(digital.ofdm_demod(
				options=grc_blks2.options(
					modulation="bpsk",
					fft_length=512,
					occupied_tones=200,
					cp_length=128,
					snr=10,
					log=None,
					verbose=None,
				),
				callback=lambda ok, payload: self.digital_ofdm_demod_0.recv_pkt(ok, payload),
			),
		)

		##################################################
		# Connections
		##################################################
		self.connect((self.digital_ofdm_demod_0, 0), (self.gr_file_sink_0, 0))
		self.connect((self.gr_file_source_0, 0), (self.gr_throttle_0, 0))
		self.connect((self.gr_throttle_0, 0), (self.digital_ofdm_demod_0, 0))

	def get_samp_rate(self):
		return self.samp_rate

	def set_samp_rate(self, samp_rate):
		self.samp_rate = samp_rate

if __name__ == '__main__':
	parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
	(options, args) = parser.parse_args()
	tb = top_block()
	tb.Run(True)

