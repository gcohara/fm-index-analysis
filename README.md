# FM Synth Modulation Index Analysis

## Intro

The variable that determines the amplitude of the sidebands in FM synthesis is known as the modulation index, and it is defined as follows:  

$$ I = \frac {\Delta f_{carrier}} {f_{modulator}} $$

When using an FM synthesiser, we control this via (generally) the 'output level' parameter of a modulating operator.  
However, different synthesisers will have different modulation indices for a given output level.  
For example, on a DX7, an output level of 85 might correspond to a modulation index of 4, while on the Opsix it might correspond to a modulation index of 6.

Generally, manufacturers don't make their output level to modulation index curves readily available.  
This repo is an attempt to experimentally determine these curves.

## Method

- Record synthesiser with 2 operators at ratio 1:1, with output levels in increments of 5%
- Apply fourier transform to get the amplitudes of the sidebands
- Use inverse Bessel functions to get modulation indices

## Resources

Chowning and Briston - FM Theory & Applications `(https://www.burnkit2600.com/manuals/fm_theory_and_applications.pdf)`