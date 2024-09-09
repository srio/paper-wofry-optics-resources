#
# Import section
#
import numpy

from syned.beamline.beamline_element import BeamlineElement
from syned.beamline.element_coordinates import ElementCoordinates
from wofry.propagator.propagator import PropagationManager, PropagationElements, PropagationParameters

from wofry.propagator.wavefront1D.generic_wavefront import GenericWavefront1D

from wofryimpl.propagator.propagators1D.fresnel import Fresnel1D
from wofryimpl.propagator.propagators1D.fresnel_convolution import FresnelConvolution1D
from wofryimpl.propagator.propagators1D.fraunhofer import Fraunhofer1D
from wofryimpl.propagator.propagators1D.integral import Integral1D
from wofryimpl.propagator.propagators1D.fresnel_zoom import FresnelZoom1D
from wofryimpl.propagator.propagators1D.fresnel_zoom_scaling_theorem import FresnelZoomScaling1D


#
# SOURCE========================
#


def run_source(my_mode_index=0):
    ##########  SOURCE ##########

    #
    # create output_wavefront
    #
    #
    output_wavefront = GenericWavefront1D.initialize_wavefront_from_range(x_min=-5e-05, x_max=5e-05,
                                                                          number_of_points=1000)
    output_wavefront.set_photon_energy(10000)
    output_wavefront.set_gaussian_hermite_mode(sigma_x=6.06643e-06, amplitude=1, mode_x=0, shift=0, beta=1.51821)
    # previous command is useless but...
    output_wavefront.set_gaussian_hermite_mode(sigma_x=6.06643e-06, amplitude=1, mode_x=my_mode_index, shift=0,
                                               beta=1.51821)
    return output_wavefront


#
# BEAMLINE========================
#


def run_beamline(output_wavefront):
    ##########  OPTICAL SYSTEM ##########

    ##########  OPTICAL ELEMENT NUMBER 1 ##########

    input_wavefront = output_wavefront.duplicate()
    from wofryimpl.beamline.optical_elements.ideal_elements.screen import WOScreen1D

    optical_element = WOScreen1D()

    # drift_before 30 m
    #
    # propagating
    #
    #
    propagation_elements = PropagationElements()
    beamline_element = BeamlineElement(optical_element=optical_element,
                                       coordinates=ElementCoordinates(p=30.000000, q=0.000000,
                                                                      angle_radial=numpy.radians(0.000000),
                                                                      angle_azimuthal=numpy.radians(0.000000)))
    propagation_elements.add_beamline_element(beamline_element)
    propagation_parameters = PropagationParameters(wavefront=input_wavefront, propagation_elements=propagation_elements)
    # self.set_additional_parameters(propagation_parameters)
    #
    propagation_parameters.set_additional_parameters('magnification_x', 20.0)
    #
    propagator = PropagationManager.Instance()
    try:
        propagator.add_propagator(FresnelZoom1D())
    except:
        pass
    output_wavefront = propagator.do_propagation(propagation_parameters=propagation_parameters,
                                                 handler_name='FRESNEL_ZOOM_1D')
    return output_wavefront


#
# MAIN FUNCTION========================
#


# def main():
#     from srxraylib.plot.gol import plot, plot_image
#     from wofryimpl.propagator.util.tally import TallyCoherentModes
#
#     tally = TallyCoherentModes()
#     for my_mode_index in range(10):
#         output_wavefront = run_source(my_mode_index=my_mode_index)
#         output_wavefront = run_beamline(output_wavefront)
#         tally.append(output_wavefront)
#
#     tally.plot_cross_spectral_density(show=1, filename="")
#     tally.plot_spectral_density(show=1, filename="")
#     tally.plot_occupation(show=1, filename="")
#
#
# #
# # MAIN========================
# #
#
#
# main()