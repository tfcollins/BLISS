%% OFDM BLISS

% First Blind Look
!LD_LIBRARY_PATH="" &&
interfere_org=read_complex_binary('BLIND.txt');

% Run receiver
!LD_LIBRARY_PATH="" &&
mixed_input=read_complex_binary('mixed.txt');
bliss_SS( mixed_input,interfere_org, fft_size );

% Run Demod and Eval
!LD_LIBRARY_PATH="" &&