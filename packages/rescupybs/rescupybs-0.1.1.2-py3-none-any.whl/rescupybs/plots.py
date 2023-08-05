import numpy as np
import matplotlib.pyplot as plt

def Nispin(eigenvalues, chpts, labels, legend, fig_p):
    plt.figure(figsize=fig_p.size)
    color = fig_p.color or ['r']
    linestyle = fig_p.linestyle or ['-']
    linewidth = fig_p.linewidth or [0.8]
    plt.plot(eigenvalues[0], color=color[0], linewidth=linewidth[0], linestyle=linestyle[0])
    plt.xlim(chpts[0],chpts[-1])
    plt.ylim(fig_p.vertical)
    plt.ylabel('Energy (eV)')
    plt.xticks(chpts,labels)
    if len(chpts) > 2:
        for i in chpts[1:-1]:
            plt.axvline(i, linewidth=0.4, linestyle='-.', c='gray')
    plt.axhline(linewidth=0.4, linestyle='-.', c='gray')
    plt.tick_params(axis='y', which='minor', color='gray')
    plt.legend(legend, frameon=False, prop={'size':'medium'}, loc=fig_p.location)
    plt.savefig(fig_p.output, dpi=fig_p.dpi, transparent=True, bbox_inches='tight')

def Mnispin(eigenvalues, chpts, labels, vbm_cbm, fig_p):
    plt.figure(figsize=fig_p.size)
    linestyle = fig_p.linestyle or ['-']
    linewidth = fig_p.linewidth or [0.8]
    VBM, CBM = vbm_cbm[0]
    org = plt.plot(eigenvalues[0], linewidth=linewidth[0], linestyle=linestyle[0])
    fig = plt.plot(eigenvalues[0,:,VBM-5:CBM+6], linewidth=linewidth[0]*1.5, linestyle=(0, (3, 1)))
    plt.xlim(chpts[0],chpts[-1])
    plt.ylim(fig_p.vertical)
    plt.ylabel('Energy (eV)')
    plt.xticks(chpts,labels)
    if len(chpts) > 2:
        for i in chpts[1:-1]:
            plt.axvline(i, linewidth=0.4, linestyle='-.', c='gray')
    plt.axhline(linewidth=0.4, linestyle='-.', c='gray')
    plt.tick_params(axis='y', which='minor', color='gray')
    plt.legend(fig, range(VBM-5, CBM+6), frameon=False, prop={'size':'medium'}, loc='center right')
    plt.savefig(fig_p.output, dpi=fig_p.dpi, transparent=True, bbox_inches='tight')

def Ispin(eigenvalues, chpts, labels, legend, fig_p):
    plt.figure(figsize=fig_p.size)
    color = fig_p.color or ['r', 'k']
    linestyle = fig_p.linestyle or ['-', '-.']
    linewidth = fig_p.linewidth or [0.8, 0.8]
    if len(color) == 1:
        color = [color[0], 'k']
    if len(linestyle) == 1:
        linestyle = [linestyle[0], '-.']
    if len(linewidth) == 1:
        linewidth = [linewidth[0], 0.8]
    p_up = plt.plot(eigenvalues[0], color=color[0], linewidth=linewidth[0], linestyle=linestyle[0])
    p_do = plt.plot(eigenvalues[1], color=color[1], linewidth=linewidth[1], linestyle=linestyle[1])
    plt.xlim(chpts[0],chpts[-1])
    plt.ylim(fig_p.vertical)
    plt.ylabel('Energy (eV)')
    plt.xticks(chpts,labels)
    if len(chpts) > 2:
        for i in chpts[1:-1]:
            plt.axvline(i, linewidth=0.4, linestyle='-.', c='gray')
    plt.axhline(linewidth=0.4, linestyle='-.', c='gray')
    plt.tick_params(axis='y', which='minor', color='gray')
    plt.legend([p_up[0], p_do[0]], ['up', 'down'], frameon=False, prop={'style':'italic', 'size':'medium'}, alignment='left', loc=fig_p.location, title=legend[0], title_fontproperties={'size':'medium'})
    plt.savefig(fig_p.output, dpi=fig_p.dpi, transparent=True, bbox_inches='tight')

def Dispin(eigenvalues, chpts, labels, legend, fig_p):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=fig_p.size)
    fig.subplots_adjust(wspace=0.0)
    color = fig_p.color or ['r', 'k']
    linestyle = fig_p.linestyle or ['-', '-.']
    linewidth = fig_p.linewidth or [0.8, 0.8]
    if len(color) == 1:
        color = [color[0], 'k']
    if len(linestyle) == 1:
        linestyle = [linestyle[0], '-.']
    if len(linewidth) == 1:
        linewidth = [linewidth[0], 0.8]
    ax1.plot(eigenvalues[0], color=color[0], linewidth=linewidth[0], linestyle=linestyle[0])
    ax2.plot(eigenvalues[1], color=color[1], linewidth=linewidth[1], linestyle=linestyle[1])
    ax1.legend(['up'], frameon=False, prop={'style':'italic', 'size':'medium'}, alignment='left', loc=fig_p.location, title=legend[0], title_fontproperties={'size':'medium'})
    ax2.legend(['down'], frameon=False, prop={'style':'italic', 'size':'medium'}, alignment='left', loc=fig_p.location)
    ax1.tick_params(axis='y', which='minor', color='gray')
    ax2.tick_params(axis='y', which='minor', color='gray')
    ax1.axhline(linewidth=0.4, linestyle='-.', c='gray')
    ax2.axhline(linewidth=0.4, linestyle='-.', c='gray')
    ax2.set_yticklabels([])
    ax1.set_xlim(chpts[0],chpts[-1])
    ax1.set_ylim(fig_p.vertical)
    ax2.set_xlim(chpts[0],chpts[-1])
    ax2.set_ylim(fig_p.vertical)
    ax1.set_ylabel('Energy (eV)')
    ax1.set_xticks(chpts,labels[:-1]+[''])
    ax2.set_xticks(chpts,labels)
    if len(chpts) > 2:
        for i in chpts[1:-1]:
            ax1.axvline(i, linewidth=0.4, linestyle='-.', c='gray')
            ax2.axvline(i, linewidth=0.4, linestyle='-.', c='gray')
    ax1.axhline(linewidth=0.4, linestyle='-.', c='gray')
    ax2.axhline(linewidth=0.4, linestyle='-.', c='gray')
    plt.savefig(fig_p.output, dpi=fig_p.dpi, transparent=True, bbox_inches='tight')

def Mispin(eigenvalues, chpts, labels, vbm_cbm, fig_p):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=fig_p.size)
    linestyle = fig_p.linestyle or ['-', '-']
    linewidth = fig_p.linewidth or [0.8, 0.8]
    fig.subplots_adjust(wspace=0.0)
    if len(linestyle) == 1:
        linestyle = [linestyle[0], linestyle[0]]
    if len(linewidth) == 1:
        linewidth = [linewidth[0], linewidth[0]]
    VBM_up, CBM_up = vbm_cbm[0]
    VBM_do, CBM_do = vbm_cbm[1]
    p_up_o = ax1.plot(eigenvalues[0], linewidth=linewidth[0], linestyle=linestyle[0])
    p_up_f = ax1.plot(eigenvalues[0,:,VBM_up-5:CBM_up+6], linewidth=linewidth[0]*1.5, linestyle=(0, (3, 1)))
    p_do_o = ax2.plot(eigenvalues[1], linewidth=linewidth[1], linestyle=linestyle[1])
    p_do_f = ax2.plot(eigenvalues[1,:,VBM_do-5:CBM_do+6], linewidth=linewidth[1]*1.5, linestyle=(0, (3, 1)))
    ax1.legend(p_up_f, range(VBM_up-5, CBM_up+6), frameon=False, prop={'size':'medium'}, alignment='left', title="up", title_fontproperties={'style':'italic', 'size':'medium'}, loc='center right')
    ax2.legend(p_do_f, range(VBM_do-5, CBM_do+6), frameon=False, prop={'size':'medium'}, alignment='left', title="down", title_fontproperties={'style':'italic', 'size':'medium'}, loc='center right')
    ax1.tick_params(axis='y', which='minor', color='gray')
    ax2.tick_params(axis='y', which='minor', color='gray')
    ax1.axhline(linewidth=0.4, linestyle='-.', c='gray')
    ax2.axhline(linewidth=0.4, linestyle='-.', c='gray')
    ax2.set_yticklabels([])
    ax1.set_xlim(chpts[0],chpts[-1])
    ax1.set_ylim(fig_p.vertical)
    ax2.set_xlim(chpts[0],chpts[-1])
    ax2.set_ylim(fig_p.vertical)
    ax1.set_ylabel('Energy (eV)')
    ax1.set_xticks(chpts,labels[:-1]+[''])
    ax2.set_xticks(chpts,labels)
    if len(chpts) > 2:
        for i in chpts[1:-1]:
            ax1.axvline(i, linewidth=0.4, linestyle='-.', c='gray')
            ax2.axvline(i, linewidth=0.4, linestyle='-.', c='gray')
    ax1.axhline(linewidth=0.4, linestyle='-.', c='gray')
    ax2.axhline(linewidth=0.4, linestyle='-.', c='gray')
    plt.savefig(fig_p.output, dpi=fig_p.dpi, transparent=True, bbox_inches='tight')

def tdos(arr, ele, legend, fig_p):
    plt.figure(figsize=fig_p.size)
    plt.minorticks_on()
    plt.tick_params(axis='both', which='minor', color='gray')
    color = fig_p.color or ['']
    linestyle = fig_p.linestyle or ['-']
    linewidth = fig_p.linewidth or [0.8]
    if fig_p.exchange:
        if color[0]:
            plt.plot(arr, ele[:,0], linewidth=linewidth[0], linestyle=linestyle[0], color=color[0])
            if fig_p.fill:
                plt.fill_between(arr, ele[:,0], 0, color=color[0], alpha=fig_p.fill)
        else:
            plt.plot(arr, ele[:,0], linewidth=linewidth[0], linestyle=linestyle[0])
            if fig_p.fill:
                plt.fill_between(arr, ele[:,0], 0, alpha=fig_p.fill)
        plt.tick_params(axis='y', labelsize='medium', labelcolor='dimgray')
        plt.xlim(fig_p.vertical)
        plt.ylim(fig_p.horizontal)
        plt.xlabel('Energy (eV)')
        plt.ylabel('Density of states, electrons/eV')
    else:
        if color[0]:
            plt.plot(ele[:,0], arr, linewidth=linewidth[0], linestyle=linestyle[0], color=color[0])
            if fig_p.fill:
                plt.fill_betweenx(arr, ele[:,0], 0, color=color[0], alpha=fig_p.fill)
        else:
            plt.plot(ele[:,0], arr, linewidth=linewidth[0], linestyle=linestyle[0])
            if fig_p.fill:
                plt.fill_betweenx(arr, ele[:,0], 0, alpha=fig_p.fill)
        plt.tick_params(axis='x', labelsize='medium', labelcolor='dimgray')
        plt.ylim(fig_p.vertical)
        plt.xlim(fig_p.horizontal)
        plt.ylabel('Energy (eV)')
        plt.xlabel('Density of states, electrons/eV')
    L = plt.legend([], frameon=False, loc=fig_p.location, title=legend[0], title_fontproperties={'size':'medium'})
    plt.gca().add_artist(L)
    plt.axvline(linewidth=0.4, linestyle='-.', c='gray')
    plt.axhline(linewidth=0.4, linestyle='-.', c='gray')
    plt.savefig(fig_p.output, dpi=fig_p.dpi, transparent=True, bbox_inches='tight')


