import numpy as np
import matplotlib.pyplot as plt
import pylab

# --- plot settings
markersize = 14

fac = 6
pylab.rcParams['figure.figsize'] = (fac * np.sqrt(2), fac)

plt.rcParams.update({'font.size': 25})
plt.rc('text', usetex=True)
plt.rc('font', family='serif')


colors = {0: '#e15759', 1: '#f28e2b', 2: '#4e79a7', 3: '#76b7b2', 4: '#59a14f',
          5: '#edc948', 6: '#b07aa1', 7: '#ff9da7', 8: '#9c755f', 9: '#bab0ac'}

def arrowed_spines(fig, ax):

    xmin, xmax = ax.get_xlim() 
    ymin, ymax = ax.get_ylim()

    # removing the default axis on all sides:
    for side in ['bottom','right','top','left']:
        ax.spines[side].set_visible(False)

    # removing the axis ticks
    plt.xticks([]) # labels 
    plt.yticks([])
    ax.xaxis.set_ticks_position('none') # tick markers
    ax.yaxis.set_ticks_position('none')

    # get width and height of axes object to compute 
    # matching arrowhead length and width
    dps = fig.dpi_scale_trans.inverted()
    bbox = ax.get_window_extent().transformed(dps)
    width, height = bbox.width, bbox.height

    # manual arrowhead width and length
    hw = 1./20.*(ymax-ymin) 
    hl = 1./20.*(xmax-xmin)
    lw = 1. # axis line width
    ohg = 0.3 # arrow overhang

    # compute matching arrowhead length and width
    yhw = hw/(ymax-ymin)*(xmax-xmin)* height/width 
    yhl = hl/(xmax-xmin)*(ymax-ymin)* width/height

    # draw x and y axis
    ax.arrow(xmin, -0.7, xmax-xmin, 0., fc='k', ec='k', lw = lw, 
             head_width=hw, head_length=hl, overhang = ohg, 
             length_includes_head= True, clip_on = False) 

    ax.arrow(0, ymin, 0., ymax-ymin, fc='k', ec='k', lw = lw, 
             head_width=yhw, head_length=yhl, overhang = ohg, 
             length_includes_head= True, clip_on = False)

def f(x):
    return (x - 1.2)**3 + 0.5 * (x - 1.5)**2

def g(x):
    return 0.1 * np.cos(30 * x) + 0.5 * (x - 1.0)**3 + 0.5 * (x - 1.5)**2 - 0.6

x0 = np.linspace(0, 2, 10)
x1 = np.linspace(0, 2, 50)


fig, ax = plt.subplots()

plt.plot(x0, [f(xi) for xi in x0])
plt.plot(x0, [f(xi) for xi in x0], 'ko')
plt.plot(x1, [g(xi) for xi in x1])
plt.plot(x1, [g(xi) for xi in x1], 'ko')


plt.text(2.0, 0.5, r'$Q(t)$')
plt.text(2.0, -0.25, r'$\psi_\alpha(t)$')

ax.annotate('', xytext=(x0[3], g(x0[3])), xy=(x0[3], f(x0[3])), arrowprops=dict(arrowstyle="->"))
plt.text(0.69, -0.1, r'\texttt{prepare()}', fontsize=15)

ax.annotate('', xytext=(x1[30], f(x1[30])), xy=(x1[30], g(x1[30])), arrowprops=dict(arrowstyle="->"))
plt.text(1.24, -0.2, r'\texttt{evaluate()}', fontsize=15)



plt.plot([x0[4], x0[4]], [0.23, 0.27], 'k')
plt.plot([x0[5], x0[5]], [0.23, 0.27], 'k')
plt.plot([x0[4], x0[5]], [0.25, 0.25], 'k')
#ax.annotate('', xytext=(x0[4], 0.25), xy=(x0[5], 0.25), arrowprops=dict(arrowstyle="<->"))
plt.text(0.97, 0.3, r'$\tau$')


plt.plot([x1[22], x1[22]], [-0.6, -0.64], 'k')
plt.plot([x1[23], x1[23]], [-0.6, -0.64], 'k')
plt.plot([x1[22], x1[23]], [-0.62, -0.62], 'k')
#ax.annotate('', xytext=(x1[20], -0.5), xy=(x1[23], -0.5), arrowprops=dict(arrowstyle="<->"))
plt.text(0.98, -0.66, r'$dt$')

plt.xlabel(r'time')
plt.ylabel(r'amplitude')

arrowed_spines(fig, ax)


plt.savefig("timescale_decoupling.png", bbox_inches='tight')

plt.show()
