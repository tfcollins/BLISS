#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Top Block
# Generated: Mon Oct  1 17:10:26 2012
##################################################

from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import fft
from gnuradio import gr
from gnuradio import window
from gnuradio.eng_option import eng_option
from gnuradio.gr import firdes
from gnuradio.wxgui import fftsink2
from grc_gnuradio import blks2 as grc_blks2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import numpy
import wx

class top_block(grc_wxgui.top_block_gui):

	def __init__(self):
		grc_wxgui.top_block_gui.__init__(self, title="Top Block")
		_icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
		self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

		##################################################
		# Variables
		##################################################
		self.samp_rate = samp_rate = 10000000

		##################################################
		# Blocks
		##################################################
		self.wxgui_fftsink2_0_0 = fftsink2.fft_sink_c(
			self.GetWin(),
			baseband_freq=0,
			y_per_div=10,
			y_divs=10,
			ref_level=0,
			ref_scale=2.0,
			sample_rate=samp_rate,
			fft_size=1024,
			fft_rate=15,
			average=False,
			avg_alpha=None,
			title="FFT Plot",
			peak_hold=False,
		)
		self.Add(self.wxgui_fftsink2_0_0.win)
		self.wxgui_fftsink2_0 = fftsink2.fft_sink_c(
			self.GetWin(),
			baseband_freq=0,
			y_per_div=10,
			y_divs=10,
			ref_level=0,
			ref_scale=2.0,
			sample_rate=samp_rate,
			fft_size=1024,
			fft_rate=15,
			average=False,
			avg_alpha=None,
			title="FFT Plot",
			peak_hold=False,
		)
		self.Add(self.wxgui_fftsink2_0.win)
		self.random_source_x_0 = gr.vector_source_b(map(int, numpy.random.randint(0, 2, 1000)), True)
		self.gr_vector_to_stream_0 = gr.vector_to_stream(gr.sizeof_gr_complex*1, 512)
		self.gr_throttle_0 = gr.throttle(gr.sizeof_gr_complex*1, samp_rate)
		self.gr_sub_xx_0 = gr.sub_cc(512)
		self.gr_stream_to_vector_0 = gr.stream_to_vector(gr.sizeof_gr_complex*1, 512)
		self.gr_file_source_1 = gr.file_source(gr.sizeof_gr_complex*512, "/home/traviscollins/git/BLISS/Matlab/Spectral_Subtraction/hilbert.txt", True)
		self.gr_file_source_0 = gr.file_source(gr.sizeof_float*1, "/home/traviscollins/git/BLISS/Matlab/Spectral_Subtraction/INPUT.txt", True)
		self.gr_file_sink_0 = gr.file_sink(gr.sizeof_float*1, "/home/traviscollins/git/BLISS/Matlab/Spectral_Subtraction/OUTPUT.txt")
		self.gr_file_sink_0.set_unbuffered(False)
		self.gr_add_xx_0 = gr.add_vcc(1)
		self.fft_vxx_1 = fft.fft_vcc(512, False, (window.blackmanharris(1024)), True, 1)
		self.fft_vxx_0 = fft.fft_vcc(512, True, (window.blackmanharris(1024)), True, 1)
		self.digital_ofdm_mod_0 = grc_blks2.packet_mod_f(digital.ofdm_mod(
				options=grc_blks2.options(
					modulation="bpsk",
					fft_length=512,
					occupied_tones=200,
					cp_length=128,
					pad_for_usrp=True,
					log=None,
					verbose=None,
				),
			),
			payload_length=0,
		)
		self.digital_ofdm_demod_0 = grc_blks2.packet_demod_f(digital.ofdm_demod(
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
		self.digital_dxpsk_mod_0 = digital.dbpsk_mod(
			samples_per_symbol=2,
			excess_bw=0.35,
			gray_coded=True,
			verbose=False,
			log=False)
			

		##################################################
		# Connections
		##################################################
		self.connect((self.gr_file_source_0, 0), (self.digital_ofdm_mod_0, 0))
		self.connect((self.digital_ofdm_demod_0, 0), (self.gr_file_sink_0, 0))
		self.connect((self.gr_stream_to_vector_0, 0), (self.fft_vxx_0, 0))
		self.connect((self.random_source_x_0, 0), (self.digital_dxpsk_mod_0, 0))
		self.connect((self.digital_ofdm_mod_0, 0), (self.gr_add_xx_0, 0))
		self.connect((self.digital_dxpsk_mod_0, 0), (self.gr_add_xx_0, 1))
		self.connect((self.gr_add_xx_0, 0), (self.gr_throttle_0, 0))
		self.connect((self.gr_throttle_0, 0), (self.gr_stream_to_vector_0, 0))
		self.connect((self.fft_vxx_0, 0), (self.gr_sub_xx_0, 0))
		self.connect((self.gr_file_source_1, 0), (self.gr_sub_xx_0, 1))
		self.connect((self.gr_vector_to_stream_0, 0), (self.digital_ofdm_demod_0, 0))
		self.connect((self.gr_vector_to_stream_0, 0), (self.wxgui_fftsink2_0, 0))
		self.connect((self.gr_add_xx_0, 0), (self.wxgui_fftsink2_0_0, 0))
		self.connect((self.gr_sub_xx_0, 0), (self.fft_vxx_1, 0))
		self.connect((self.fft_vxx_1, 0), (self.gr_vector_to_stream_0, 0))

	def get_samp_rate(self):
		return self.samp_rate

	def set_samp_rate(self, samp_rate):
		self.samp_rate = samp_rate
		self.wxgui_fftsink2_0.set_sample_rate(self.samp_rate)
		self.wxgui_fftsink2_0_0.set_sample_rate(self.samp_rate)

if __name__ == '__main__':
	parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
	(options, args) = parser.parse_args()
	tb = top_block()
	tb.Run(True)

