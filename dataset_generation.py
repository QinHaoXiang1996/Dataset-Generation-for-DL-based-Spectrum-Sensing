#!/usr/bin/env python
from transmitters import transmitters
from source_alphabet import source_alphabet
import analyze_stats
from gnuradio import channels, gr, blocks
import numpy as np
import numpy.fft, cPickle, gzip
import random
dataset = {}
nvecs_per_key = 10000 # the number of samples which represent hypothesis H1
vec_length = 128 # vec_length means sample length
snr_vals = range(-20,6,1)
alphabet_type = 'discrete'



print('sample_length is :%d'%vec_length)
for snr in snr_vals:
    print("snr is %d"%snr)
    for i,mod_type in enumerate(transmitters[alphabet_type]):
        # the modulation types are set in transmitter.py
        insufficient_modsnr_vectors = True
        modvec_indx = 0# modvec_indx means the total number of samples
        dataset[(mod_type.modname,snr)]=np.zeros([nvecs_per_key,vec_length,2],dtype=np.float32)
        dataset[(mod_type.modname,snr,'noise')]=np.zeros([nvecs_per_key,vec_length,2],dtype=np.float32)
        # when insufficient_modsnr_vectors is "true", we use GNU radio to get a  discrete time sequence
        # the simulation method is proposed in "T. O’Shea and N. West, “Radio machine learning dataset generation with gnu radio,” in Proc. GNU Radio Conference (GRCon16), vol. 1, 2016."
        while insufficient_modsnr_vectors:
            tx_len = int(10e3)
            if mod_type.modname == "QAM16":
                tx_len = int(20e3)
            if mod_type.modname == "QAM64":
                tx_len = int(30e3)
            src = source_alphabet(alphabet_type, tx_len, True)
            mod = mod_type()
            fD = 1
            delays = [0.0, 0.9, 1.7]
            mags = [1, 0.8, 0.3]
            ntaps = 8
            noise_amp = 10**(-snr/10.0)
            chan = channels.dynamic_channel_model( 200e3, 0.01, 50, .01, 0.5e3, 8, fD, True,4, delays, mags, ntaps, noise_amp, 0x1337 )
            snk = blocks.vector_sink_c()
            tb = gr.top_block()
            # connect blocks
            tb.connect(src, mod,chan, snk)
            tb.run()
            raw_output_vector = np.array(snk.data(), dtype=np.complex64)
            #now we collect samples randomly from the discrete time sequence
            sampler_indx = random.randint(50, 500)
            while sampler_indx + vec_length < len(raw_output_vector) and modvec_indx < nvecs_per_key:
                sampled_vector = raw_output_vector[sampler_indx:sampler_indx+vec_length]
                signal_energy = np.sum(np.abs(sampled_vector)**2)
                snr_x=(10**(snr/10.0))
                xpower=signal_energy/np.size(sampled_vector)
                npower=xpower/snr_x
                random_noise = (np.random.randn(vec_length)+1j*np.random.randn(vec_length))*np.sqrt(npower)
                noise_energy = np.sum(np.abs(random_noise)**2)
                random_noise = random_noise / (noise_energy**0.5)
                total_energy = np.sum(np.abs(sampled_vector)**2)
                total_vector = sampled_vector / (total_energy**0.5) #energy normalization
                dataset[(mod_type.modname, snr)][modvec_indx,:,0] = np.real(total_vector)
                dataset[(mod_type.modname, snr)][modvec_indx,:,1] = np.imag(total_vector)
                dataset[(mod_type.modname, snr,'noise')][modvec_indx, :, 0] = np.real(random_noise)
                dataset[(mod_type.modname, snr,'noise')][modvec_indx, :, 1] = np.imag(random_noise)
                sampler_indx += random.randint(vec_length, round(len(raw_output_vector)*.05))
                modvec_indx += 1
            if modvec_indx == nvecs_per_key:
            # we're all done
                insufficient_modsnr_vectors = False
print("all done. writing to disk")
cPickle.dump(dataset, file('data_'+str(vec_length)+'.pkl', "wb" ) )

