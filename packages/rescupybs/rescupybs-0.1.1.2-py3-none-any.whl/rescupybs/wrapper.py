import argparse, os, re, platform, glob
import matplotlib.pyplot as plt
import numpy as np
from rescupybs import plots, functions
from rescupy.utils import read_field
from rescupybs import __version__

plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['ytick.minor.visible'] = True
plt.rcParams["mathtext.fontset"] = 'cm'

class cla_fig:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if isinstance(value, str):
                exec('self.%s = "%s"' %(key, value))
            else:
                exec('self.%s = %s' %(key, value))

def main():
    parser = argparse.ArgumentParser(description='Plot the band structure from rescuplus calculation result *.json or *.dat file.',
                                     epilog='''
Example:
rescubs -y -0.5 0.5 -b
''',
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-v', "--version",    action="version",     version="rescupybs "+__version__+" from "+os.path.dirname(__file__)+' (python'+platform.python_version()+')')
    parser.add_argument('-s', "--size",       type=float, nargs=2,  help='figure size: width, height')
    parser.add_argument('-b', "--divided",    action='store_true',  help="plot the up and down spin in divided subplot")
    parser.add_argument('-y', "--vertical",   type=float, nargs=2,  help="vertical axis")
    parser.add_argument('-g', "--legend",     type=str,   nargs=1,  help="legend labels")
    parser.add_argument('-L', "--location",   type=str.lower,       default='best',
                                                                    choices=['best', 'upper right', 'upper left', 'lower left', 'lower right', 'right', 'center left', 'center right', 'lower center', 'upper center', 'center'],
                                                                    help="arrange the legend location, default best")
    parser.add_argument('-c', "--color",      type=str,             nargs='+', help="line color: b, blue; g, green; r, red; c, cyan; m, magenta; y, yellow;"+
                                                                                    "k, black; w, white", default=[])
    parser.add_argument('-k', "--linestyle",  type=str,             nargs='+', help="linestyle: solid, dashed, dashdot, dotted or tuple; default: solid",
                                                                                    default=[])
    parser.add_argument('-w', "--linewidth",  type=str,             nargs='+', help="linewidth, default: 0.8", default=[])
    parser.add_argument('-m', "--modify",     type=int, nargs=2,    help='modify the bands overlap, the up or nonispin bands to exchange values')
    parser.add_argument('-n', "--nbands",     type=int, nargs=2,    help='the down bands to exchange values')
    parser.add_argument('-i', "--input",      type=str,             nargs='+', default=[], help="plot figure from .json or .dat file")
    parser.add_argument('-o', "--output",     type=str,             default="BAND.png", help="filename of the figure, default: BAND.png")
    parser.add_argument('-q', "--dpi",        type=int,             default=500, help="dpi of the figure, default: 500")
    parser.add_argument('-l', "--labels",     type=str.upper,       nargs='+', default=[], help='labels for high-symmetry points')
    parser.add_argument('-d', "--dos",        type=str,             nargs='?', default='', help="plot DOS from .json file, default: nano_dos_out.json")
    parser.add_argument('-x', "--horizontal", type=float, nargs=2,  help="Density of states, electrons/eV range")
    parser.add_argument('-a', "--exchange",   action='store_true',  help="exchange the x and y axes of DOS")
    parser.add_argument('-p', "--partial",    type=str,             nargs='+', default=[], help='the partial DOS to plot, s p d')
    parser.add_argument('-e', "--elements",   type=str,             nargs='+', default=[], help="PDOS labels")
    parser.add_argument('-W', "--wratios",    type=float,           help='width ratio for DOS subplot')
    parser.add_argument('-z', "--fill",       type=float,           nargs='?', help='fill a shaded region between PDOS and axis, default: 0.2', default=None,
                                                                                    const=0.2, metavar="alpha")
    parser.add_argument('-f', "--font",       type=str,             default='STIXGeneral', help="font to use")

    args = parser.parse_args()

    labels_f = [re.sub("'|‘|’", '′', re.sub('"|“|”', '″', re.sub('^GA[A-Z]+$|^G$', 'Γ', i))) for i in args.labels]
    elements = [re.sub("'|‘|’", '′', re.sub('"|“|”', '″', i)) for i in args.elements]
    if args.dos != '':
        dosfiles = args.dos or 'nano_dos_out.json'
        if dosfiles.rsplit('.',1)[0].endswith('_in'):
            dosfiles = dosfiles.rsplit('_in',1)[0]+'_out.json'
        if os.path.isdir(dosfiles):
            dosfiles = os.path.join(dosfiles, 'nano_dos_out.json')
        dosfiles = dosfiles if os.path.exists(dosfiles) else None
    else:
        dosfiles = None

    color = []
    for i in args.color:
        j = i.split('*')
        if len(j) == 2:
            color += [ast.literal_eval(j[0])] * int(j[1]) if '(' in j[0] and ')' in j[0] else [j[0]] * int(j[1])
        else:
            color += [ast.literal_eval(i)] if '(' in i and ')' in i else [i]

    linestyle = []
    for i in args.linestyle:
        j = i.split('*')
        if len(j) == 2:
            linestyle += [ast.literal_eval(j[0])] * int(j[1]) if '(' in j[0] and ')' in j[0] else [j[0]] * int(j[1])
        else:
            linestyle += [ast.literal_eval(i)] if '(' in i and ')' in i else [i]

    linewidth = []
    for i in args.linewidth:
        j = i.split('*')
        linewidth += [float(j[0])] * int(j[1]) if len(j) == 2 else [float(i)]

    plt.rcParams['font.family'] = '%s'%args.font

    pltname = os.path.split(os.getcwd())[-1]

    input = args.input or ['nano_bs_out.json']
    input = [f for i in input for f in glob.glob(i)]
    input = [os.path.join(i,'nano_bs_out.json') if os.path.isdir(i) else i for i in input]
    input = [i for i in input if os.path.exists(i)]

    width_ratios = args.wratios or (0.3 if args.divided else 0.5)

    fig_p = cla_fig(output=args.output, size=args.size, vertical=args.vertical, horizontal=args.horizontal,
                    color=color, linestyle=linestyle, linewidth=linewidth, location=args.location, dpi=args.dpi,
                    width_ratios=width_ratios, exchange=args.exchange, fill=args.fill)

    len_bandfile = len(input)
# plot Band Structure
    if len_bandfile == 1:
        if not fig_p.vertical:
            fig_p.vertical = [-5.0, 5.0]
        if input[0].lower().endswith('.json'):
            if 'bs' in input[0].split('_'):
                bs_file = input[0]
                eigenvalues, chpts, labels = functions.bs_json_read(bs_file)
                if labels_f:
                    labels = labels_f
                legend = args.legend or [pltname]
                if len(chpts) > len(labels):
                    labels = labels + [''] * (len(chpts) - len(labels))
                elif len(chpts) < len(labels):
                    labels = labels[:len(chpts)]
                if len(eigenvalues) == 1:
                    plots.Nispin(eigenvalues, chpts, labels, legend, fig_p)
                elif len(eigenvalues) == 2 and not args.divided:
                    plots.Ispin(eigenvalues, chpts, labels, legend, fig_p)
                elif len(eigenvalues) == 2 and args.divided:
                    plots.Dispin(eigenvalues, chpts, labels, legend, fig_p)

        elif input[0].lower().endswith('.dat'):
            eigenvalues = functions.bs_dat_read(input)
            chpts, labels, vbm_cbm = functions.labels_read("LABELS")
            if labels_f:
                labels = labels_f
            legend = args.legend or [pltname]
            if len(chpts) > len(labels):
                labels = labels + [''] * (len(chpts) - len(labels))
            elif len(chpts) < len(labels):
                labels = labels[:len(chpts)]
            if args.modify:
                if args.modify[0] != args.modify[1]:
                    functions.exchange(eigenvalues[0,:,args.modify[0]], eigenvalues[0,:,args.modify[1]])
                    np.savetxt(input[0], eigenvalues[0])
                plots.Mnispin(eigenvalues, chpts, labels, vbm_cbm, fig_p)
            else:
                plots.Nispin(eigenvalues, chpts, labels, legend, fig_p)

    elif len_bandfile == 2:
        if not fig_p.vertical:
            fig_p.vertical = [-5.0, 5.0]
        Extension = [f.rsplit('.', 1)[-1].lower() for f in input]
        if all(x == Extension[0] for x in Extension):
            if len(input) == 2 and Extension[0] == 'dat':
                eigenvalues = functions.bs_dat_read(input)
                chpts, labels, vbm_cbm = functions.labels_read("LABELS")
                if labels_f:
                    labels = labels_f
                legend = args.legend or [pltname]
                if len(chpts) > len(labels):
                    labels = labels + [''] * (len(chpts) - len(labels))
                elif len(chpts) < len(labels):
                    labels = labels[:len(chpts)]
                if args.modify or args.nbands:
                    if args.modify and args.modify[0] != args.modify[1]:
                        functions.exchange(eigenvalues[0,:,args.modify[0]], eigenvalues[0,:,args.modify[1]])
                        np.savetxt(input[0], eigenvalues[0])
                    if args.nbands and args.nbands[0] != args.nbands[1]:
                        functions.exchange(eigenvalues[0,:,args.nbands[0]], eigenvalues[0,:,args.nbands[1]])
                        np.savetxt(input[1], eigenvalues[1])
                    plots.Mispin(eigenvalues, chpts, labels, vbm_cbm, fig_p)
                else:
                    if len(eigenvalues) == 2 and not args.divided:
                        plots.Ispin(eigenvalues, chpts, labels, legend, fig_p)
                    elif len(eigenvalues) == 2 and args.divided:
                        plots.Dispin(eigenvalues, chpts, labels, legend, fig_p)
            elif Extension[0] == 'json' and all('bs' in f.split('_') for f in input):
                eigenvalues, chpts, labels = functions.bs_json_read_all(input)
                if labels_f:
                    labels = labels_f
                legend = args.legend or [pltname]
                if len(chpts) > len(labels):
                    labels = labels + [''] * (len(chpts) - len(labels))
                elif len(chpts) < len(labels):
                    labels = labels[:len(chpts)]
                if len(eigenvalues) == 1:
                    plots.Nispin(eigenvalues, chpts, labels, legend, fig_p)
                elif len(eigenvalues) == 2 and not args.divided:
                    plots.Ispin(eigenvalues, chpts, labels, legend, fig_p)
                elif len(eigenvalues) == 2 and args.divided:
                    plots.Dispin(eigenvalues, chpts, labels, legend, fig_p)
        else:
            raise Exception("The input files mismatch.")
# plot DOS
    elif len_bandfile == 0:
        if dosfiles:
            if fig_p.output == "BAND.png":
                fig_p.output = "DOS.png"
            legend = args.legend or [pltname]
            arr, ele = functions.tdos(dosfiles)
            plots.tdos(arr, ele, legend, fig_p)
        else:
            print("ERROR: No *dos_out.json file.")
    else:
        if not fig_p.vertical:
            fig_p.vertical = [-5.0, 5.0]
        Extension = [f.rsplit('.', 1)[-1].lower() for f in input]
        if all(x == Extension[0] for x in Extension) and Extension[0] == 'json' and all('bs' in f.split('_') for f in input):
            eigenvalues, chpts, labels = functions.bs_json_read_all(input)
            if labels_f:
                labels = labels_f
            legend = args.legend or [pltname]
            if len(chpts) > len(labels):
                labels = labels + [''] * (len(chpts) - len(labels))
            elif len(chpts) < len(labels):
                labels = labels[:len(chpts)]
            if len(eigenvalues) == 1:
                plots.Nispin(eigenvalues, chpts, labels, legend, fig_p)
            elif len(eigenvalues) == 2 and not args.divided:
                plots.Ispin(eigenvalues, chpts, labels, legend, fig_p)
            elif len(eigenvalues) == 2 and args.divided:
                plots.Dispin(eigenvalues, chpts, labels, legend, fig_p)
        else:
            print("Input file mismatch.")

def surface():
    parser = argparse.ArgumentParser(description='Export the wavefunction isosurface for VESTA from rescuplus calculation result *.json and *.h5 files.',
                                     epilog='''
Example:
rescuiso -b 1 -k 0
''',
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-v', "--version", action="version", version="rescupybs "+__version__+" from "+os.path.dirname(__file__)+' (python'+platform.python_version()+')')
    parser.add_argument('-i', "--input",   type=str,         nargs='+', default=[],  help="export the wavefunction isosurface from .json and .h5 files")
    parser.add_argument('-o', "--output",  type=str,         help="wavefunction isosurface for VESTA format")
    parser.add_argument('-k', "--kpt",     type=int,         nargs='+', default=[0], help="The kpoint in wavefunctions")
    parser.add_argument('-b', "--band",    type=int,         nargs='+', default=[0], help="The band in wavefunctions")
    parser.add_argument('-s', "--spin",    type=int,         default=1, help="The up or down spin in wavefunctions")

    args = parser.parse_args()

    if args.kpt[0] < 0 or args.band[0] < 0:
        raise Exception("Illegal input of kpt.")

    input = args.input or ['nano_wvf_out.json']
    input = [f.rsplit('_in',1)[0]+'_out.json' if f.rsplit('.',1)[0].endswith('in') else f for i in input for f in glob.glob(i)]
    input = [os.path.join(i,'nano_wvf_out.json') if os.path.isdir(i) else i for i in input]
    input = [i.rsplit('.',1)[0] for i in input]
    input = [i for i in input if os.path.exists(i+'.json') and os.path.exists(i+'.h5')]
    if not input:
        raise Exception("The input file does not exist.")

    if len(input) == 1:
        if 'wvf' in input[0].split('_'):
            functions.isosurfaces_wf(input[0], args.output, args.kpt, args.band, args.spin)
        elif 'dos' in input[0].split('_'):
            functions.isosurfaces_dos(input[0], args.output)
    else:
        if all('wvf' in f.split('_') for f in input):
            for i in range(len(input)):
                functions.isosurfaces_wf(input[i], args.output, args.kpt, args.band, args.spin)

