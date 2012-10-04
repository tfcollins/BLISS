%% OFDM



%% import signals
wanted_org=read_complex_binary('/home/traviscollins/git/BLISS/GNURadio/OFDM/transmitted.txt');
interfere_org=read_complex_binary('/home/traviscollins/git/BLISS/GNURadio/OFDM/transmitted_int.txt');
fft_size=2^15;
output=[];

for i=1:fft_size:length(interfere_org)-fft_size
wanted=wanted_org(i:i+fft_size-1);
interfere=interfere_org(i:i+fft_size-1);

fs=10e6;
time=length(interfere)/fs;

% Convoluted Signal
received=wanted+awgn(interfere,30,'measured');

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
disp(['Error : ',num2str(error/fft_size)]);
disp(['ErrorW: ',num2str(error2/fft_size)]);

% Save processed data
output=[output; xh];

end

%Save to file
filename='/home/traviscollins/git/BLISS/GNURadio/OFDM/received_p.txt';
f = fopen (filename, 'w');
output_f=[real(output) imag(output)];
len=length(output_f)*2;
output_f = reshape (output_f.',len,1);
fwrite(f, output_f,'float');
fclose (f);

