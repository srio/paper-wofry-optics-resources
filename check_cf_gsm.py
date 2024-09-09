import numpy

beta = numpy.linspace(0, 10, 100)

# beta = CF / numpy.sqrt(1-CF)

CF = 1 - 1 / (1 + beta**2 / 2 + beta * numpy.sqrt((beta/2)**2+1))
from srxraylib.plot.gol import plot

beta2 = CF / numpy.sqrt(1-CF)

plot(beta, CF, beta2, CF, xtitle='beta', ytitle='cf')
