%% OFDM BLISS

% First Blind Look
!LD_
interfere_org=read_complex_binary('BLIND.txt');

% Run receiver
!LD_
mixed_input=read_complex_binary('mixed.txt');
bliss_SS( mixed_input,interfere_org, fft_size );

% Run Demod and Eval
!LD_