!sudo sysctl -w net.core.rmem_max=50000000
!sudo sysctl -w net.core.wmem_max=1048576
for i=1:10
%% Run USRP Receiver
unix('python /home/traviscollins/data/Models/USRP_Receiver/receiver.py');

%% Read File
%received
r=read_complex_binary('/home/traviscollins/data/Models/USRP_Receiver/received_data_C.txt');
%known symbols
s_saved=read_complex_binary('/home/traviscollins/data/pre.txt');

%% Process Data
cor=abs(xcorr(r(1:500),prea));
%remove padding
cor=cor(length(r(1:500))-length(prea):end);
stem(cor)
%find first preamble
[indexs,~]=find(cor>=floor(max(cor)*100)/100);

%[~,indexs]=find(cor>=floor(max(cor)));
%[~,indexs]=max(cor);

if size(indexs,2)==0
    break
end
first=indexs(1);
if (first>length(prea))
    start=first-length(prea);
elseif length(indexs)>1
    first=indexs(2);
    if (first>length(prea))
        start=first-length(prea);
    else
        continue
    end
else
    continue
end

r_saved=r;
r=r(start:start+length(prea)-1)';
s=s_saved;
prea=s(10:110);
s=prea.';

%equalizer2
n=9;                               % length of equalizer - 1
%n=50;
delta=0;                           % use delay <=n*length(b)
p=length(r)-delta;
R=toeplitz(r(n+1:p),r(n+1:-1:1));  % build matrix R
S=s(n+1-delta:p-delta)';           % and vector S
f=inv(R'*R)*R'*S;                   % calculate equalizer f
Jmin=S'*S-S'*R*inv(R'*R)*R'*S;      % Jmin for this f and delta
result=filter(f,1,r_saved);                   % equalizer is a filter


%% Write Output
filename='processed_data_C.txt';
f = fopen (filename, 'w');
output_f=[real(result) imag(result)];
len=length(output_f)*2;
output_f = reshape (output_f.',len,1);
fwrite(f, output_f,'float');
fclose (f);
disp(['Done']);

unix('python /home/traviscollins/data/Models/Demoder/demoder.py');

end