# FM Synth Modulation Index Analysis

## Aim

Produce a graph like the one below, but for the Korg Opsix

![dx7_graph](images/chowning_dx7_index_graph)

## Intro

The variable that determines the amplitude of the sidebands in FM synthesis is known as the modulation index, and it is defined as follows:  

$$ I = \frac {\Delta f_{carrier}} {f_{modulator}} $$

When using an FM synthesiser, we control this via (generally) the 'output level' parameter of a modulating operator.  
However, different synthesisers will have different modulation indices for a given output level.  
For example, on a DX7, an output level of 85 might correspond to a modulation index of 4, while on the Opsix it might correspond to a modulation index of 6.

Generally, manufacturers don't make their output level to modulation index curves readily available.  
This repo is an attempt to experimentally determine these curves.

## Method

- Determine by listening for settings where fundamental is zero, these are rough guidelines that will be needed for root finding algorithm.
- Record synthesiser with 2 operators at ratio 1:3, with output levels in increments of 5%
- Remove any DC offsets
- Slice the file for each amplitude level
- Normalise files to just under 0.0dB
- Apply fourier transform to get the amplitudes of the fundamental frequency
- Use inverse Bessel functions to get modulation indices

## Issues encountered

It's better if we don't use operators at ratio 1:1. Because if we do we get interference from negative frequency sidebands!  
Inverse Bessel functions don't exist. Need to use some root finding algorithm  

## Resources

Chowning and Briston - FM Theory & Applications `(https://www.burnkit2600.com/manuals/fm_theory_and_applications.pdf)`
