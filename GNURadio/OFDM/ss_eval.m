index=0;
error=zeros(1,length(.1:.1:20));
for SNR=.1:.1:20
    index=index+1;
   error(index)=spectral_subtraction(2^9,SNR);
end


semilogy(SNR,error);