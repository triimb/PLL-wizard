import math

def get_design_pll(dic_constraints):

    #Constraints
    Kvco = dic_constraints['Kvco']
    Icp = dic_constraints['Icp']
    Fin = dic_constraints['Fin']
    Fout = dic_constraints['Fout']
    Vdd = dic_constraints['Vdd']

    #Values
    wref = 2*math.pi*Fin
    wc = 0.7*wref/10
    phiM = 60
    wp = 3.73*wc
    wz = 0.268*wc
    N = Fout/Fin
    C1 = (wz/wp)*((Icp*2*math.pi*Kvco)/(math.pow(wc, 2)*N))*((math.sqrt(math.pow(1+(wc/wz),2)))/(math.sqrt(math.pow(1+(wc/wp),2))))
    C2 = C1*(wp/wz-1)
    R2 = 1/(C2*wz)
    delta_f = 2*Fout
    Fmin = Fout-0.8*Fout
    Fmax = Fout + 0.8 * Fout
    mark = Fmax/Vdd
    space = Fmin

    #Res
    dic_design_parameters = {
        'wref' : round(wref, 2),
        'wc' : round(wc, 2),
        'phiM' : phiM,
        'wp' : round(wp,2),
        'wz' : round(wz, 2),
        'N' : N,
        'C1' : C1,
        'C2' : C2,
        'R2' : R2,
        'delta_f' : delta_f,
        'Fmin' : int(Fmin),
        'Fmax' : int(Fmax),
        'mark' : int(mark),
        'space' : int(space)
    }

    return dic_design_parameters

def get_all_paramaters(dic_constraints, dic_design_parameters):
    dic_design_parameters.update(dic_constraints)
    return dic_design_parameters

def get_default_constraints_and_unit():
        return {
                "Kvco" : [3e8, "Hz/V"],
                "Icp": [1e-4, "A"],
                "Fin": [2e7, "Hz"],
                "Fout": [5e9, "Hz"],
                "Vdd": [3.3, "V"]
            }

def get_default_constraints():
    return {key : value[0] for key, value in get_default_constraints_and_unit().items()}

def get_results_paramaters_names():
    return {
            'wref': 'rad/s',
            'wc': 'rad/s',
            'ΦM': '°',
            'wp': 'rad/s',
            'wz': 'rad/s',
            'N': '',
            'C1': 'F',
            'C2': 'F',
            'R2': 'Ω',
            'delta_f': 'Hz',
            'Fmin': 'Hz',
            'Fmax': 'Hz',
            'mark' : '',
            'space' : ''
        }

def get_abbaque_phase_margin():
    "key : phase margin ; value : D1%"
    return {
            45: 30,
            30: 45,
            20: 60,
            10: 90,
            5: 150
            }
