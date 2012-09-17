#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Demoder
# Generated: Mon Sep 17 12:24:42 2012
##################################################

from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.gr import firdes
from grc_gnuradio import blks2 as grc_blks2
from optparse import OptionParser

class demoder(gr.top_block):

	def __init__(self):
		gr.top_block.__init__(self, "Demoder")

		##################################################
		# Variables
		##################################################
		self.samp_rate = samp_rate = 32000

		##################################################
		# Blocks
		##################################################
		self.gr_throttle_0 = gr.throttle(gr.sizeof_gr_complex*1, samp_rate)
		self.gr_head_0 = gr.head(gr.sizeof_gr_complex*1, 1024*5)
		self.gr_file_source_0 = gr.file_source(gr.sizeof_gr_complex*1, "/home/traviscollins/data/Models/USRP_Receiver/processed_data_C.txt", True)
		self.gr_file_sink_0 = gr.file_sink(gr.sizeof_char*1, "/home/traviscollins/data/Models/Demoder/demod_data_B.txt")
		self.gr_file_sink_0.set_unbuffered(False)
		self.digital_dxpsk_demod_0 = digital.dbpsk_demod(
			samples_per_symbol=2,
			excess_bw=0.35,
			freq_bw=6.28/100.0,
			phase_bw=6.28/100.0,
			timing_bw=6.28/100.0,
			gray_coded=True,
			verbose=False,
			log=False
		)
		self.blks2_packet_decoder_0 = grc_blks2.packet_demod_b(grc_blks2.packet_decoder(
				access_code="",
				threshold=-1,
				callback=lambda ok, payload: self.blks2_packet_decoder_0.recv_pkt(ok, payload),
			),
		)

		##################################################
		# Connections
		##################################################
		self.connect((self.gr_head_0, 0), (self.digital_dxpsk_demod_0, 0))
		self.connect((self.digital_dxpsk_demod_0, 0), (self.blks2_packet_decoder_0, 0))
		self.connect((self.blks2_packet_decoder_0, 0), (self.gr_file_sink_0, 0))
		self.connect((self.gr_file_source_0, 0), (self.gr_throttle_0, 0))
		self.connect((self.gr_throttle_0, 0), (self.gr_head_0, 0))

	def get_samp_rate(self):
		return self.samp_rate

	def set_samp_rate(self, samp_rate):
		self.samp_rate = samp_rate

if __name__ == '__main__':
	parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
	(options, args) = parser.parse_args()
	if gr.enable_realtime_scheduling() != gr.RT_OK:
		print "Error: failed to enable realtime scheduling."
	tb = demoder()
	tb.run()

