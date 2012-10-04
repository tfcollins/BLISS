%% Load signals
spec=read_complex_binary('FFT_Pre.txt');
spec2=spec(1:512);
spec=interp(spec2,10);
spec=(spec);

%% view first fft
occupied_tones=256*10;
fft_length=512*10;
fs=100e3;
left=spec((fft_length-occupied_tones)/2+1:fft_length/2);
right=spec(fft_length/2+1:(fft_length+occupied_tones)/2);

band_size=10;
bins=zeros(1,length(left));
bins2=zeros(1,length(left));

for i=1:band_size:length(left)-band_size-1
   bins(i:i+band_size-1)=mean(left(i:i+band_size-1));
end

for i=1:band_size:length(right)-band_size-1
   bins2(i:i+band_size-1)=mean(right(i:i+band_size-1));
end


bins=[zeros(1,(fft_length-occupied_tones)/2), bins, bins2, zeros(1,(fft_length-occupied_tones)/2)];
%center bins
bins=[bins(band_size/2+1:end)*3 zeros(1,band_size/2)];


%whiten
% [d2,p2] = lpc(bins,512);
% 
% bins=filter(-d2(2:end),1,bins);

result=spec-bins.';


% % These loops reduce the impact of musical noise on the signal
% Beta_MN=.1;
% for i = 1:length(result)
%     if result(i)<0
%         result(i) = 0;
%     end
% end
% 
% for i = 1:length(result)
%     if result(i) < Beta_MN*spec(i)
%         result(i) = Beta_MN*spec(i);
%     end
% end



subplot(3,1,1);
hold on
plot(real(spec));
plot(real(bins),'r');
ylim([-40 40]);
hold off

subplot(3,1,2);
plot(real(result),'g');
ylim([-40 40]);


subplot(3,1,3);
hold on
hilbert_R=real(hilbert(real(spec)));
hilbert_I=real(hilbert(imag(spec)));
hilbert_R=hilbert_R+hilbert_I*1i;
plot(real(hilbert_R),'r');

hilbert_R=downsample(hilbert_R,10);
result2=spec2-hilbert_R;

plot(real(result2),'g');
ylim([-40 40]);
hold off


%% overlap freq bins
filename='hilbert.txt';
f = fopen (filename, 'w');
output_f=[real(hilbert_R) imag(hilbert_R)];
len=length(output_f)*2;
output_f = reshape (output_f.',len,1);
fwrite(f, output_f,'float');
fclose (f);

