function [ errors ] = spectral_subtraction( fft_size, SNR)
%% OFDM



%% import signals
wanted_org=read_complex_binary('/home/traviscollins/git/BLISS/GNURadio/OFDM/transmitted.txt');
interfere_org=read_complex_binary('/home/traviscollins/git/BLISS/GNURadio/OFDM/transmitted_int.txt');
%fft_size=2^15;
errors=[];

for i=1:fft_size:length(interfere_org)-fft_size
wanted=wanted_org(i:i+fft_size-1);
interfere=interfere_org(i:i+fft_size-1);

fs=10e6;
time=length(interfere)/fs;

% Convoluted Signal
received=wanted+awgn(interfere,SNR,'measured');

%% Create envelope of interferer

interfere_fft=fft(interfere,fft_size);

interfere_fft_real=real(interfere_fft);
interfere_fft_imag=imag(interfere_fft);

int_real_env=real(hilbert(interfere_fft_real));
int_imag_env=real(hilbert(interfere_fft_imag));


%% FFT 
received_fft=fft(received,fft_size);

received_fft_real=real(received_fft);
received_fft_imag=imag(received_fft);


%% Subtract
result_fft=(received_fft_real-int_real_env)+(received_fft_imag-int_imag_env)*1i;
result=ifft(result_fft);

%% whiten
result=received;
[d2,p2] = lpc(result,7);
xh=filter(-d2(2:end),1,result);

%% Evaluate
error=sum(sign(real(result))-sign(real(wanted)));
error2=sum(sign(real(xh))-sign(real(wanted)));

% Save processed data
errors=[errors; abs(error2/fft_size)];

end

errors=mean(errors);


end

