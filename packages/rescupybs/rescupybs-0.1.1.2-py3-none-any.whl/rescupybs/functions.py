import numpy as np
import h5py, re, pint, os
from rescupy.totalenergy import TotalEnergy
from ase import Atoms as ats
from ase.io import read, write

ureg = pint.UnitRegistry(system="atomic")

# rescubs

def exchange(array_a,array_b):
    l=len(array_a)
    m=np.arange(l)
    for i in range(2,l):
        fun1=np.polyfit(m[i-2:i], array_a[i-2:i], 1)
        fun2=np.polyfit(m[i-2:i], array_b[i-2:i], 1)
        p1=np.poly1d(fun1)
        p2=np.poly1d(fun2)
        if abs(p1(m[i])-array_a[i]) > abs(p1(m[i])-array_b[i]) or abs(p2(m[i])-array_b[i]) > abs(p2(m[i])-array_a[i]):
            array_a[i], array_b[i]=array_b[i], array_a[i]

def bs_json_read(bs_file):
    calc = TotalEnergy.read(bs_file)
    chpts = calc.system.kpoint.special_points
    labels = calc.system.kpoint.get_special_points_labels()
    eigenvalues = calc.energy.eigenvalues.T - calc.energy.efermi
    ispin = calc.system.hamiltonian.ispin
    formula = calc.system.atoms.formula
    filename = bs_file.rsplit('.', 1)[0]
    for i in range(0, len(chpts)-1):
        if chpts[i] + 1 == chpts[i+1] and labels[i] == labels[i+1]:
            j = chpts[i]
            eigenvalues = np.delete(eigenvalues, j, axis=1)
            del chpts[i]
            del labels[i]
            for k in range(i, len(chpts)):
                chpts[k] = chpts[k] - 1
        if i + 2 >= len(chpts):
            break
    labels = [i.replace('G', 'Γ') for i in labels]
    if ispin == 2:
        np.savetxt(filename+'_bs_up.dat',eigenvalues[0])
        np.savetxt(filename+'_bs_down.dat',eigenvalues[1])
        up_vb, up_vbm, up_cb, up_cbm = get_vbm_cbm(eigenvalues[0])
        metal_up = 'May be metal.' if ismetal(eigenvalues[0]) else ''
        do_vb, do_vbm, do_cb, do_cbm = get_vbm_cbm(eigenvalues[1])
        metal_do = 'May be metal.' if ismetal(eigenvalues[1]) else ''
        up_vbm_cbm = [up_vb, up_vbm, up_cb, up_cbm, "ev, spin_up, Band gap:", up_cbm-up_vbm, metal_up]
        do_vbm_cbm = [do_vb, do_vbm, do_cb, do_cbm, "ev, spin_do, Band gap:", do_cbm-do_vbm, metal_do]
        with open('LABELS', "w") as f:
            f.writelines([str(i)+' ' for i in chpts]+['\n'])
            f.writelines([i+' ' for i in labels]+['\n'])
            f.writelines(formula+'\n')
            f.writelines([str(i)+' ' for i in up_vbm_cbm]+['\n'])
            f.writelines([str(i)+' ' for i in do_vbm_cbm]+['\n'])
    else:
        np.savetxt(filename+'_bs.dat',eigenvalues[0])
        vb, vbm, cb, cbm = get_vbm_cbm(eigenvalues[0])
        metal = 'May be metal.' if ismetal(eigenvalues[0]) else ''
        vbm_cbm_l = [vb, vbm, cb, cbm, "ev, Band gap:", cbm-vbm, metal]
        with open('LABELS', "w") as f:
            f.writelines([str(i)+' ' for i in chpts]+['\n'])
            f.writelines([i+' ' for i in labels]+['\n'])
            f.writelines(formula+'\n')
            f.writelines([str(i)+' ' for i in vbm_cbm_l]+['\n'])
    return eigenvalues, chpts, labels

def bs_json_read_all(input):
    for i in range(len(input)):
        calc = TotalEnergy.read(input[i])
        if i == 0:
            chpts = calc.system.kpoint.special_points
            labels = calc.system.kpoint.get_special_points_labels()
            eigenvalues = calc.energy.eigenvalues.T - calc.energy.efermi
            ispin = calc.system.hamiltonian.ispin
            formula = calc.system.atoms.formula
        else:
            chpts = chpts + [i + chpts[-1] + 1 for i in calc.system.kpoint.special_points]
            labels = labels + calc.system.kpoint.get_special_points_labels()
            eigenvalues = np.concatenate((eigenvalues, calc.energy.eigenvalues.T - calc.energy.efermi), axis=1)
    filename = os.path.commonprefix([os.path.split(i)[-1] for i in input]).rsplit('.',1)[0]
    if not filename:
        filename = 'nano_bs_out'
    filename = filename.strip('_')
    for i in range(0, len(chpts)-1):
        if chpts[i] + 1 == chpts[i+1] and labels[i] == labels[i+1]:
            j = chpts[i]
            eigenvalues = np.delete(eigenvalues, j, axis=1)
            del chpts[i]
            del labels[i]
            for k in range(i, len(chpts)):
                chpts[k] = chpts[k] - 1
        if i + 2 >= len(chpts):
            break
    labels = [i.replace('G', 'Γ') for i in labels]
    if ispin == 2:
        np.savetxt(filename+'_bs_up.dat',eigenvalues[0])
        np.savetxt(filename+'_bs_down.dat',eigenvalues[1])
        up_vb, up_vbm, up_cb, up_cbm = get_vbm_cbm(eigenvalues[0])
        metal_up = 'May be metal.' if ismetal(eigenvalues[0]) else ''
        do_vb, do_vbm, do_cb, do_cbm = get_vbm_cbm(eigenvalues[1])
        metal_do = 'May be metal.' if ismetal(eigenvalues[1]) else ''
        up_vbm_cbm = [up_vb, up_vbm, up_cb, up_cbm, "ev, spin_up, Band gap:", up_cbm-up_vbm, metal_up]
        do_vbm_cbm = [do_vb, do_vbm, do_cb, do_cbm, "ev, spin_do, Band gap:", do_cbm-do_vbm, metal_do]
        with open('LABELS', "w") as f:
            f.writelines([str(i)+' ' for i in chpts]+['\n'])
            f.writelines([i+' ' for i in labels]+['\n'])
            f.writelines(formula+'\n')
            f.writelines([str(i)+' ' for i in up_vbm_cbm]+['\n'])
            f.writelines([str(i)+' ' for i in do_vbm_cbm]+['\n'])
    else:
        np.savetxt(filename+'_bs.dat',eigenvalues[0])
        vb, vbm, cb, cbm = get_vbm_cbm(eigenvalues[0])
        metal = 'May be metal.' if ismetal(eigenvalues[0]) else ''
        vbm_cbm_l = [vb, vbm, cb, cbm, "ev, Band gap:", cbm-vbm, metal]
        with open('LABELS', "w") as f:
            f.writelines([str(i)+' ' for i in chpts]+['\n'])
            f.writelines([i+' ' for i in labels]+['\n'])
            f.writelines(formula+'\n')
            f.writelines([str(i)+' ' for i in vbm_cbm_l]+['\n'])
    return eigenvalues, chpts, labels

def bs_dat_read(input):
    data = []
    for i in input:
        data.append(np.loadtxt(i))
    return np.array(data)

def labels_read(LABELS):
    with open(LABELS, "r") as main_file:
        lines = main_file.readlines()
    chpts = [int(i) for i in lines[0].split()]
    labels = [i for i in lines[1].split()]
    if len(lines) > 4:
        str0 = lines[3].split()
        str1 = lines[4].split()
        vbm_cbm = [[int(str0[0]), int(str0[2])], [int(str1[0]), int(str1[2])]]
    else:
        str = lines[3].split()
        vbm_cbm = [[int(str[0]), int(str[2])]]
    return chpts, labels, vbm_cbm

def ismetal(eigenvalues_s):
    issemi = np.all(eigenvalues_s < 0.0, axis=0)
    issemi = np.logical_or(issemi, np.all(eigenvalues_s > 0.0, axis=0) )
    return not np.all(issemi)

def get_vbm_cbm(eigenvalues_s):
    max = np.max(eigenvalues_s[eigenvalues_s < 0.0])
    min = np.min(eigenvalues_s[eigenvalues_s > 0.0])
    i, vb = np.where(eigenvalues_s==max)
    i, cb = np.where(eigenvalues_s==min)
    return vb[0], max, cb[0], min

def dos(filename):
    from rescupy import DensityOfStates as DOS
    from rescupy.jsonio import json_read
    calc = DOS.from_totalenergy(filename)
    calc.set_units('atomic')
    cal  = json_read(filename)
    calc.dos.dos = np.array([cal['dos']['dos']]).T
    calc.dos.energy = np.array(cal['dos']['energy'])
    calc.dos.efermi = cal['dos']['efermi']
    if cal['dos']['pdos_return']:
        calc.dos.orbA = cal['dos']['orbA']
        calc.dos.orbL = cal['dos']['orbL']
        calc.dos.orbM = cal['dos']['orbM']
        h5name = filename.rsplit('.json')[0] + '.h5'
        h = h5py.File(h5name, mode="r")
        fld = h['dos']['pdos']['total'][0:]
        fld = np.transpose(fld, [i for i in range(fld.ndim - 1, -1, -1)])
        calc.dos.pdos = fld
        calc.dos.pdos_return = cal['dos']['pdos_return']
    calc.set_units('si')
    return calc

def tdos(dosfiles):
    calc = dos(dosfiles)
    arr = calc.dos.energy
    efe = calc.dos.efermi
    ele = calc.dos.dos
    return arr - efe, ele

# rescuiso

def isosurfaces_wf(input, output, kpt, band, spin):
    calc = TotalEnergy.read(input+'.json')
    kpt_l = len(kpt)
    band_l = len(band)
    if kpt_l == 1 and band_l == 1:
        if not output:
            output = input+'_'+str(kpt[0])+'_'+str(band[0])+'_'+str(spin)+'.vasp'
        if calc.system.hamiltonian.ispin == 1:
            att = f"wavefunctions/{kpt[0] + 1}/field"
        else:
            if spin == 1:
                att = f"wavefunctions/spin-up/{kpt[0] + 1}/field"
            else:
                att = f"wavefunctions/spin-down/{kpt[0] + 1}/field"
        print("Reading *.h5 file ...")
        filename = input+'.h5'
        h = h5py.File(filename, mode="r")
        print("Processing data ...")
        fld = h[att][0:]
        fld = np.transpose(fld, [i for i in range(fld.ndim - 1, -1, -1)])
        fld = np.asfortranarray(fld)
        fld = fld / ureg.bohr**1.5
        fld = fld[::2, :] + 1j * fld[1::2, :]
        fld.ito("angstrom ** -1.5")
        if band[0] < fld.shape[-1]:
            fld = fld[..., band[0]].magnitude
        else:
            raise Exception("The band is out of range in *.h5 file.")
        f_abs = np.abs(fld)
        f_div = np.where(np.abs(np.angle(fld)) < np.pi / 2, f_abs, -f_abs)
        f_div = np.reshape(f_div, (f_div.shape[-1], -1), order='F').T
    elif kpt_l == 2 and band_l == 1:
        if not kpt[0] < kpt[1]:
            raise Exception("Illegal input of kpt.")
        if not output:
            output = input+'_'+str(kpt[0])+'-'+str(kpt[1])+'_'+str(band[0])+'_'+str(spin)+'.vasp'
        nkpts = kpt[1] - kpt[0] + 1
        att = [''] * nkpts
        for i in range(kpt[0], kpt[1] + 1):
            if calc.system.hamiltonian.ispin == 1:
                att[i] = f"wavefunctions/{i + 1}/field"
            else:
                if spin == 1:
                    att[i] = f"wavefunctions/spin-up/{i + 1}/field"
                else:
                    att[i] = f"wavefunctions/spin-down/{i + 1}/field"
        print("Reading *.h5 file ...")
        filename = input+'.h5'
        h = h5py.File(filename, mode="r")
        print("Processing data ...")
        for i in range(nkpts):
            fld_i = h[att[i]][0:]
            if i == 0:
                fld = fld_i
            else:
                fld += fld_i
        fld = np.transpose(fld, [i for i in range(fld.ndim - 1, -1, -1)])
        fld = np.asfortranarray(fld)
        fld = fld / ureg.bohr**1.5
        fld = fld[::2, :] + 1j * fld[1::2, :]
        fld.ito("angstrom ** -1.5")
        if band[0] < fld.shape[-1]:
            fld = fld[..., band[0]].magnitude
        else:
            raise Exception("The band is out of range in *.h5 file.")
        f_abs = np.abs(fld)
        f_div = np.where(np.abs(np.angle(fld)) < np.pi / 2, f_abs, -f_abs)
        f_div = np.reshape(f_div, (f_div.shape[-1], -1), order='F').T
    elif kpt_l == 1 and band_l == 2:
        if not band[0] < band[1]:
            raise Exception("Illegal input of band.")
        if not output:
            output = input+'_'+str(kpt[0])+'_'+str(band[0])+'-'+str(band[1])+'_'+str(spin)+'.vasp'
        if calc.system.hamiltonian.ispin == 1:
            att = f"wavefunctions/{kpt[0] + 1}/field"
        else:
            if spin == 1:
                att = f"wavefunctions/spin-up/{kpt[0] + 1}/field"
            else:
                att = f"wavefunctions/spin-down/{kpt[0] + 1}/field"
        print("Reading *.h5 file ...")
        filename = input+'.h5'
        h = h5py.File(filename, mode="r")
        print("Processing data ...")
        fld = h[att][0:]
        fld = np.transpose(fld, [i for i in range(fld.ndim - 1, -1, -1)])
        fld = np.asfortranarray(fld)
        fld = fld / ureg.bohr**1.5
        fld = fld[::2, :] + 1j * fld[1::2, :]
        fld.ito("angstrom ** -1.5")
        if band[1] < fld.shape[-1]:
            for i in range(band[0], band[1] + 1):
                if i == band[0]:
                    fld_i = fld[..., i].magnitude
                else:
                    fld_i += fld[..., i].magnitude
            fld = fld_i
        else:
            raise Exception("The band is out of range in *.h5 file.")
        f_abs = np.abs(fld)
        f_div = np.where(np.abs(np.angle(fld)) < np.pi / 2, f_abs, -f_abs)
        f_div = np.reshape(f_div, (f_div.shape[-1], -1), order='F').T
    elif kpt_l == 2 and band_l == 2:
        if not kpt[0] < kpt[1]:
            raise Exception("Illegal input of kpt.")
        if not band[0] < band[1]:
            raise Exception("Illegal input of band.")
        if not output:
            output = input+'_'+str(kpt[0])+'-'+str(kpt[1])+'_'+str(band[0])+'-'+str(band[1])+'_'+str(spin)+'.vasp'
        nkpts = kpt[1] - kpt[0] + 1
        att = [''] * nkpts
        for i in range(kpt[0], kpt[1] + 1):
            if calc.system.hamiltonian.ispin == 1:
                att[i] = f"wavefunctions/{i + 1}/field"
            else:
                if spin == 1:
                    att[i] = f"wavefunctions/spin-up/{i + 1}/field"
                else:
                    att[i] = f"wavefunctions/spin-down/{i + 1}/field"
        print("Reading *.h5 file ...")
        filename = input+'.h5'
        h = h5py.File(filename, mode="r")
        print("Processing data ...")
        for i in range(nkpts):
            fld_i = h[att[i]][0:]
            if i == 0:
                fld = fld_i
            else:
                fld += fld_i
        fld = np.transpose(fld, [i for i in range(fld.ndim - 1, -1, -1)])
        fld = np.asfortranarray(fld)
        fld = fld / ureg.bohr**1.5
        fld = fld[::2, :] + 1j * fld[1::2, :]
        fld.ito("angstrom ** -1.5")
        if band[1] < fld.shape[-1]:
            for i in range(band[0], band[1] + 1):
                if i == band[0]:
                    fld_i = fld[..., i].magnitude
                else:
                    fld_i += fld[..., i].magnitude
            fld = fld_i
        else:
            raise Exception("The band is out of range in *.h5 file.")
        f_abs = np.abs(fld)
        f_div = np.where(np.abs(np.angle(fld)) < np.pi / 2, f_abs, -f_abs)
        f_div = np.reshape(f_div, (f_div.shape[-1], -1), order='F').T
    else:
        raise Exception("Illegal input.")
    print("Reading structure ...")
    pbc = [1, 1, 1]
    positions = calc.system.atoms.positions
    cell = calc.system.cell.avec
    elements_symbols = calc.system.atoms.get_labels()
    stp = ats(elements_symbols,positions=positions,cell=cell,pbc=pbc)
    grid = calc.system.cell.grid
    print("Saving data to disk ...")
    write(output, stp, direct=True, vasp5=True)
    with open(output, "a") as f:
        f.writelines(['\n']+[str(i)+' ' for i in grid]+['\n'])
        np.savetxt(f, f_div)

def isosurfaces_dos(input, output):
    calc = TotalEnergy.read(input+'.json')
    if not output:
        output = input+'.vasp'
    att = f"density/total"
    print("Reading *.h5 file ...")
    filename = input+'.h5'
    h = h5py.File(filename, mode="r")
    print("Processing data ...")
    fld = h[att][0:]
    fld = np.transpose(fld, [i for i in range(fld.ndim - 1, -1, -1)])
    fld = np.asfortranarray(fld)
    fld = fld / ureg.bohr**3
    fld.ito("angstrom ** -3")
    fld = fld.magnitude
    f_abs = np.abs(fld)
    f_div = np.where(np.abs(np.angle(fld)) < np.pi / 2, f_abs, -f_abs)
    f_div = np.reshape(f_div, (f_div.shape[-1], -1), order='F').T
    print("Reading structure ...")
    pbc = [1, 1, 1]
    positions = calc.system.atoms.positions
    cell = calc.system.cell.avec
    elements_symbols = calc.system.atoms.get_labels()
    stp = ats(elements_symbols,positions=positions,cell=cell,pbc=pbc)
    grid = calc.system.cell.grid
    print("Saving data to disk ...")
    write(output, stp, direct=True, vasp5=True)
    with open(output, "a") as f:
        f.writelines(['\n']+[str(i)+' ' for i in grid]+['\n'])
        np.savetxt(f, f_div)
