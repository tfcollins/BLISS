#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Receiver
# Generated: Mon Sep 17 12:25:26 2012
##################################################

from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.gr import firdes
from optparse import OptionParser

class receiver(gr.top_block):

	def __init__(self):
		gr.top_block.__init__(self, "Receiver")

		##################################################
		# Variables
		##################################################
		self.samp_rate = samp_rate = 100000

		##################################################
		# Blocks
		##################################################
		self.uhd_usrp_source_0 = uhd.usrp_source(
			device_addr="",
			stream_args=uhd.stream_args(
				cpu_format="fc32",
				channels=range(1),
			),
		)
		self.uhd_usrp_source_0.set_samp_rate(samp_rate)
		self.uhd_usrp_source_0.set_center_freq(2.4e9, 0)
		self.uhd_usrp_source_0.set_gain(15, 0)
		self.gr_pll_carriertracking_cc_0 = gr.pll_carriertracking_cc(1.5*3.1459/200, 2, -2)
		self.gr_head_0 = gr.head(gr.sizeof_gr_complex*1, 1024*100)
		self.gr_file_sink_0 = gr.file_sink(gr.sizeof_gr_complex*1, "/home/traviscollins/data/Models/USRP_Receiver/received_data_C.txt")
		self.gr_file_sink_0.set_unbuffered(False)

		##################################################
		# Connections
		##################################################
		self.connect((self.gr_head_0, 0), (self.gr_file_sink_0, 0))
		self.connect((self.uhd_usrp_source_0, 0), (self.gr_pll_carriertracking_cc_0, 0))
		self.connect((self.gr_pll_carriertracking_cc_0, 0), (self.gr_head_0, 0))

	def get_samp_rate(self):
		return self.samp_rate

	def set_samp_rate(self, samp_rate):
		self.samp_rate = samp_rate
		self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)

if __name__ == '__main__':
	parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
	(options, args) = parser.parse_args()
	if gr.enable_realtime_scheduling() != gr.RT_OK:
		print "Error: failed to enable realtime scheduling."
	tb = receiver()
	tb.run()

