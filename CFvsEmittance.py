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
    output_wavefront.set_gaussian_hermite_mode(sigma_x=6.06643e-06, amplitude=1, mode_x=8, shift=0, beta=1.51821)
    # previous command is useless but...
    output_wavefront.set_gaussian_hermite_mode(sigma_x=6.06643e-06, amplitude=1, mode_x=my_mode_index, shift=0,
                                               beta=1.51821)
    return output_wavefront


def cmd(sigma=1e-6, sigmap=1e-6, scan_direction='H'):
    #
    # BEAMLINE========================
    #
    from wofryimpl.propagator.util.undulator_coherent_mode_decomposition_1d import UndulatorCoherentModeDecomposition1D

    coherent_mode_decomposition = UndulatorCoherentModeDecomposition1D(
        electron_energy=6,
        electron_current=0.2,
        undulator_period=0.02,
        undulator_nperiods=100,
        K=1.19,
        photon_energy=10000,
        abscissas_interval=0.00025,
        number_of_points=1000,
        distance_to_screen=100,
        magnification_x_forward=100,
        magnification_x_backward=0.01,
        scan_direction=scan_direction,
        sigmaxx=sigma,
        sigmaxpxp=sigmap,
        useGSMapproximation=False,
        e_energy_dispersion_flag=0,
        e_energy_dispersion_sigma_relative=0.001,
        e_energy_dispersion_interval_in_sigma_units=6,
        e_energy_dispersion_points=11)

    # make calculation
    coherent_mode_decomposition_results = coherent_mode_decomposition.calculate()

    return coherent_mode_decomposition.get_eigenvalue(0) / \
           coherent_mode_decomposition.get_eigenvalues().sum()

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

def calculate_cfs(factor_h=1.0, factor_v=1.0):
    # factor_h = 0.5
    # factor_v = 15

    sigma_u = 4.856e-6
    sigma_up = 3.842e-6
    sigma_h = 30.184e-6    * numpy.sqrt(factor_h) #* factor_h
    sigma_v = 3.63641e-06  * numpy.sqrt(factor_v) #* factor_v
    sigma_hp = 4.36821e-06 * numpy.sqrt(factor_h)
    sigma_vp = 1.37498e-06 * numpy.sqrt(factor_v)

    Sigma_h = numpy.sqrt(sigma_u ** 2 + sigma_h ** 2)
    Sigma_v = numpy.sqrt(sigma_u ** 2 + sigma_v ** 2)
    Sigma_hp = numpy.sqrt(sigma_up ** 2 + sigma_hp ** 2)
    Sigma_vp = numpy.sqrt(sigma_up ** 2 + sigma_vp ** 2)

    print("Sigma_h, Sigma_hp: ", 1e6 * Sigma_h, 1e6 * Sigma_hp)
    print("Sigma_v, Sigma_vp: ", 1e6*Sigma_v, 1e6*Sigma_vp)
    cf_gsm_h = sigma_u * sigma_up / (Sigma_h * Sigma_hp)
    cf_gsm_v = sigma_u * sigma_up / (Sigma_v * Sigma_vp)
    print("CF H: ", cf_gsm_h)
    print("CF V: ", cf_gsm_v)

    cf_cmd_h = cmd(sigma_h, sigma_hp)
    # cf_cmd_v = cmd(sigma_v, sigma_vp)

    print("eps, CF CMD, GSM H: ", 1e12 * sigma_h * sigma_hp, 1e2 * cf_cmd_h, 1e2 * cf_gsm_h)
    # print("eps, CF CMD, GSM V: ", 1e12 * sigma_v * sigma_vp, 1e2 * cf_cmd_v, 1e2 * cf_gsm_v)
    return 1e12 * sigma_h * sigma_hp, 1e2 * cf_cmd_h, 1e2 * cf_gsm_h

#
# MAIN========================
#

if __name__ == "__main__":
    import matplotlib.pylab as plt
    plt.rcParams.update({'font.size': 16})
    plt.rcParams.update({'figure.figsize': (10, 6)})

    from srxraylib.plot.gol import plot
    # from srxraylib.plot.gol import plot, plot_image
    # from wofryimpl.propagator.util.tally import TallyCoherentModes
    #
    # tally = TallyCoherentModes()
    # for my_mode_index in range(10):
    #     output_wavefront = run_source(my_mode_index=my_mode_index)
    #     output_wavefront = run_beamline(output_wavefront)
    #     tally.append(output_wavefront)
    #
    # tally.plot_cross_spectral_density(show=1, filename="")
    # tally.plot_spectral_density(show=1, filename="")
    # tally.plot_occupation(show=1, filename="")

    # H

    do_calculation = 0

    if do_calculation:
        # factor = numpy.linspace(5./131.85005064, 200.0/131.85005064, 101)
        factor_h = numpy.linspace(0.01 / 131.85005064, 250 / 131.85005064, 51)

        EPS = numpy.zeros_like(factor_h)
        CF_CMD = numpy.zeros_like(factor_h)
        CF_GSM = numpy.zeros_like(factor_h)


        for i in range(factor_h.size):
            eps, cf_cmd, cf_gsm = calculate_cfs(factor_h[i], 1.0)
            EPS[i] = eps
            CF_CMD[i] = cf_cmd
            CF_GSM[i] = cf_gsm

        if True:
            f = open('CFvsEmittance.dat','w')
            for i in range(factor_h.size):
                f.write("%g  %g  %g\n" % (EPS[i], CF_CMD[i], CF_GSM[i]))
            f.close()
            print("File check_approximated_cf.dat written to disk.")

        plot(EPS, 1e-2 * CF_CMD,
             EPS, 1e-2 * CF_GSM,
             legend=['CMD','GSM'], xtitle="Horizontal emittance [pm]", ytitle='Coherent Fraction',
             title='U20 4m @ 10 keV')
    else:
        a = numpy.loadtxt('CFvsEmittance.dat')
        EPS = a[:, 0]
        CF_CMD = a[:, 1]
        CF_GSM = a[:, 2]
        plot(EPS, 1e-2 * CF_CMD,
             EPS, 1e-2 * CF_GSM,
             legend=['CMD','GSM'], xtitle="Horizontal emittance [pm]", ytitle='Coherent Fraction',
             title='U20 4m @ 10 keV', show=0)
        plt.savefig("CFvsEmittance.pdf")
        plt.show()

    sigma_u = 4.856e-6
    sigma_up = 3.842e-6
    sigma_h = 30.184e-6
    sigma_v = 3.63641e-06
    sigma_hp = 4.36821e-06
    sigma_vp = 1.37498e-06

    print("eps H: ", 1e12 * sigma_h * sigma_hp)
    print("eps V: ", 1e12 * sigma_v * sigma_vp)