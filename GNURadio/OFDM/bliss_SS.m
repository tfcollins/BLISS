function [ filename ] = bliss_SS( mixed_input,interfere_org, fft_size )

%BLISS Spectral Subtraction
%% import signals
output=[];

for i=1:fft_size:length(interfere_org)-fft_size
interfere=interfere_org(i:i+fft_size-1);

% Convoluted Signal
received=mixed_input;

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
[d2,p2] = lpc(result,7);
xh=filter(-d2(2:end),1,result);

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




end

