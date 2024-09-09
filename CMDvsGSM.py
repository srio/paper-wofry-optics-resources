

from GSM_H import run_source     as run_source_GSM_H
from GSM_H import run_beamline as run_beamline_GSM_H
from CMD_H import run_source     as run_source_CMD_H
from CMD_H import run_beamline as run_beamline_CMD_H


from GSM_V import run_source     as run_source_GSM_V
from GSM_V import run_beamline as run_beamline_GSM_V
from CMD_V import run_source     as run_source_CMD_V
from CMD_V import run_beamline as run_beamline_CMD_V

from srxraylib.plot.gol import plot, plot_image, plot_show
from wofryimpl.propagator.util.tally import TallyCoherentModes

if __name__ == "__main__":

    do_propagate = 0

    import numpy

    import matplotlib.pylab as plt
    plt.rcParams.update({'font.size': 16})
    plt.rcParams.update({'figure.figsize': (6, 6)})


    if do_propagate:
        prop_txt = "-propagated"
    else:
        prop_txt = ""



    #
    tally_CMD_H = TallyCoherentModes()
    for my_mode_index in range(50):
        output_wavefront = run_source_CMD_H(my_mode_index=my_mode_index)
        if do_propagate: output_wavefront = run_beamline_CMD_H(output_wavefront)
        tally_CMD_H.append(output_wavefront)

    #
    tally_GSM_H = TallyCoherentModes()
    for my_mode_index in range(50):
        output_wavefront = run_source_GSM_H(my_mode_index=my_mode_index)
        if do_propagate: utput_wavefront = run_beamline_GSM_H(output_wavefront)
        tally_GSM_H.append(output_wavefront)

    #
    tally_GSM_V = TallyCoherentModes()
    for my_mode_index in range(50):
        output_wavefront = run_source_GSM_V(my_mode_index=my_mode_index)
        if do_propagate: output_wavefront = run_beamline_GSM_V(output_wavefront)
        tally_GSM_V.append(output_wavefront)


    #
    tally_CMD_V = TallyCoherentModes()
    for my_mode_index in range(50):
        output_wavefront = run_source_CMD_V(my_mode_index=my_mode_index)
        if do_propagate: output_wavefront = run_beamline_CMD_V(output_wavefront)
        tally_CMD_V.append(output_wavefront)

    #
    #
    #

    x_GSM_H = tally_GSM_H.get_abscissas()
    sd_GSM_H = tally_GSM_H.get_spectral_density()
    sd_GSM_H /= sd_GSM_H.max()


    x_CMD_H = tally_CMD_H.get_abscissas()
    sd_CMD_H = tally_CMD_H.get_spectral_density()
    sd_CMD_H /= sd_CMD_H.max()

    x_GSM_V = tally_GSM_V.get_abscissas()
    sd_GSM_V = tally_GSM_V.get_spectral_density()
    sd_GSM_V /= sd_GSM_V.max()

    x_CMD_V = tally_CMD_V.get_abscissas()
    sd_CMD_V = tally_CMD_V.get_spectral_density()
    sd_CMD_V /= sd_CMD_V.max()


    # tally_GSM_H.plot_cross_spectral_density(show=1, filename="")
    # tally_CMD_H.plot_cross_spectral_density(show=1, filename="")
    # tally_GSM_V.plot_cross_spectral_density(show=1, filename="")
    # tally_CMD_V.plot_cross_spectral_density(show=1, filename="")

    # csd_GSM_H.get_cross_spectral_density()
    # csd_CMD_H.get_cross_spectral_density()
    # csd_GSM_V.get_cross_spectral_density()
    # csd_CMD_V.get_cross_spectral_density()
    #
    # csd = self.get_cross_pectral_density()

    #watch typo in tally!
    plot_image(numpy.abs(tally_CMD_H.get_cross_pectral_density()), 1e6 * x_CMD_H, 1e6 * x_CMD_H,
               title="", xtitle="x1 [um]", ytitle="z2 [um]", show=0, add_colorbar=0)
    plt.savefig("CMD_H%s.png" % prop_txt)
    plot_image(numpy.abs(tally_GSM_H.get_cross_pectral_density()), 1e6 * x_GSM_H, 1e6 * x_GSM_H,
               title="", xtitle="x1 [um]", ytitle="z2 [um]", show=0, add_colorbar=0)
    plt.savefig("GSM_H%s.png" % prop_txt)
    plot_image(numpy.abs(tally_CMD_V.get_cross_pectral_density()), 1e6 * x_CMD_V, 1e6 * x_CMD_V,
               title="", xtitle="x1 [um]", ytitle="z2 [um]", show=0, add_colorbar=0)
    plt.savefig("CMD_V%s.png" % prop_txt)
    plot_image(numpy.abs(tally_GSM_V.get_cross_pectral_density()), 1e6 * x_GSM_V, 1e6 * x_GSM_V,
               title="", xtitle="x1 [um]", ytitle="z2 [um]", show=0, add_colorbar=0)
    plt.savefig("GSM_V%s.png" % prop_txt)

    plot_show()

    plt.rcParams.update({'figure.figsize': (10, 6)})

    plot(1e6 * x_CMD_H, sd_CMD_H,
         1e6 * x_GSM_H, sd_GSM_H,
         xtitle="x [um]", ytitle="Spectral Density [arbitratry units]", legend=['CMD','GSM'], show=0)

    plt.savefig("SD_H%s.png" % prop_txt)

    plot(1e6 * x_CMD_V, sd_CMD_V,
         1e6 * x_GSM_V, sd_GSM_V,
         xtitle="z [um]", ytitle="Spectral Density [arbitratry units]", legend=['CMD','GSM'], show=0)
    plt.savefig("SD_V%s.png" % prop_txt)

    plot_show()