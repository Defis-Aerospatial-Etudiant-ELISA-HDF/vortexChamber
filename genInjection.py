import os
import sys
import math
import argparse

def clear():
    if name := os.name == "posix":
        cmd = 'clear'
    elif name == "nt":
        cmd = "cls"
    else:
        print(f"Unknown os name: {name}")
        return
    os.system(cmd)

# Paramètres des fluides
# ======================

# Debit massique [kg/s]
mdot_N2O = 22.66036029
mdot_C2H5 = 11.33018014
mdot_tot = mdot_C2H5 + mdot_N2O

# Fraction massique
Y_N2O = mdot_N2O / mdot_tot
Y_C2H5 = mdot_C2H5 / mdot_tot

# Densité [kg/m³]
rho_N2O = 1223
rho_C2H5 = 789


# Paramètres des injecteurs
# =========================

# Geometrie
r = lambda d : d/2
area = lambda d : math.pi * (d/2)**2






def compute_injection_parameters(duration=1e-3, n_inj=2, dI_N2O=2e-3, dI_C2H5=2e-3):


    # Velocity - N2O
    volume_flow_rate_N2O = mdot_N2O / rho_N2O   # Q (m³/s)
    velocity_N2O = volume_flow_rate_N2O / (area(dI_N2O)*n_inj)  # u = Q / A

    # Velocity - C2H5
    volume_flow_rate_C2H5 = mdot_C2H5 / rho_C2H5   # Q (m³/s)
    velocity_C2H5 = volume_flow_rate_C2H5 / (area(dI_C2H5)*n_inj)  # u = Q / A

    # Total injectée (kg)
    mass_total = mdot_tot * duration                                 # (kg)
    volume_total = (volume_flow_rate_N2O + volume_flow_rate_C2H5) * duration # (m³)

    return_dict = dict()
    return_dict["geometry"] = {"N2O":dI_N2O,"C2H5":dI_C2H5}
    return_dict["volume_flow_rate"] = {"N2O":volume_flow_rate_N2O,"C2H5":volume_flow_rate_C2H5}
    return_dict["velocity"] = {"N2O":velocity_N2O,"C2H5":velocity_C2H5}
    return_dict["n_inj"] = n_inj
    return_dict["duration"] = duration
    return_dict["mass_total"] = mass_total
    return_dict["volume_total"] = volume_total
    return return_dict


def show_injections_parameters(geometry,volume_flow_rate,velocity,duration,n_inj,volume_total,mass_total):

    print("===== Paramètres d'injection OpenFOAM =====")
    print(f"Débit massique {mdot_tot:.4f} [kg/s] :")
    print(f"\t(N2O)   : {mdot_N2O:.4f} [kg/s]")
    print(f"\t(C2H5)  : {mdot_C2H5:.4f} [kg/s]")
    print(f"Densité :")
    print(f"\t(N2O)   : {rho_N2O:.4f} [kg/m³]")
    print(f"\t(C2H5)  : {rho_C2H5:.4f} [kg/m³]")
    print(f"Injecteurs :")
    print(f"\tDiamètre (N2O)  : {r(geometry["N2O"])*2*1e3:.2f} [mm]")
    print(f"\tDiamètre (C2H5) : {r(geometry["C2H5"])*2*1e3:.2f} [mm]")
    print(f"\tSurface (N2O)  : {area(geometry["N2O"])*1e6:.2f} [mm²]")
    print(f"\tSurface (C2H5) : {area(geometry["C2H5"])*1e6:.2f} [mm²]")
    print(f"Nombre d'injecteur : {n_inj*2}")
    print(f"Durée d'injection  : {duration:.3f} [s]")
    print()
    print("============= Données Totales =============")
    print(f"Volume injecté {volume_total*1e6:.6f} [cm³] :")
    print(f"\t(N2O)   : {volume_flow_rate["N2O"]*1e6*duration:.4f} [cm³]")
    print(f"\t(C2H5)  : {volume_flow_rate["C2H5"]*1e6*duration:.4f} [cm³]")
    print(f"Masse injectée {mass_total:.6f} [kg] :")
    print(f"\t(N2O)   : {mdot_N2O*duration:.4f} [kg]")
    print(f"\t(C2H5)  : {mdot_C2H5*duration:.4f} [kg]")
    print()
    print("========== Données Par Injecteur ==========")
    print(f"Volume injecté {volume_total*1e6/n_inj:.6f} [cm³] :")
    print(f"\t(N2O)   : {volume_flow_rate["N2O"]*1e6*duration/n_inj:.4f} [cm³]")
    print(f"\t(C2H5)  : {volume_flow_rate["C2H5"]*1e6*duration/n_inj:.4f} [cm³]")
    print(f"Masse injectée {mass_total/n_inj:.6f} [kg] :")
    print(f"\t(N2O)   : {mdot_N2O*duration/n_inj:.4f} [kg]")
    print(f"\t(C2H5)  : {mdot_C2H5*duration/n_inj:.4f} [kg]")
    print(f"Vitesse d'injection :")
    print(f"\t(N2O)   : {velocity["N2O"]:.4f} [m/s]")
    print(f"\t(C2H5)  : {velocity["C2H5"]:.4f} [m/s]")
    print()

def compute_vec(norm):
    """ Pour un angle de 45° """
    x = math.cos(math.pi/4) * norm
    print(f"(0 +-{x:.3f} -{x:.3f})")

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest="cmd")

    parser.add_argument("--clear",action='store_true')

    generalInfo = subparser.add_parser("infos")
    generalInfo.add_argument("--duration",type=float,help="duration, default to 1ms", default=1e-3)
    generalInfo.add_argument("--n_inj",type=int,help="number of injector, for each liquid", default=1)
    generalInfo.add_argument("--dI_N2O",type=float,help="diameter of N2O's injector",default=2e-3)
    generalInfo.add_argument("--dI_C2H5",type=float,help="diameter of C2H5's injector",default=2e-3)

    vect = subparser.add_parser("vec")
    vect.add_argument("norm",type=float,help="norm of velocity")

    args = parser.parse_args()

    if args.clear:
        clear()

    if args.cmd == "infos":
        lInfos = compute_injection_parameters(args.duration, args.n_inj, args.dI_N2O, args.dI_C2H5)
        show_injections_parameters(**lInfos)
    
    elif args.cmd == "vec":
        compute_vec(args.norm)