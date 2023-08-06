"""Sample on B-modes."""
import time
import pickle
from matplotlib import pyplot as plt
from mpi4py import MPI
from cobaya.run import run
from cobaya.log import LoggedError
import numpy as np
from lilit import LiLit
from lilit import CAMBres2dict
import camb

debug = False
name = "BB"
lmax = 191

outfile = "/home/jack/Documents/data/fullsky_cov.pkl"
with open(outfile, "rb") as f:
    fullsky_covariance = pickle.load(f)

outfile = "/home/jack/Documents/data/masked_cov.pkl"
with open(outfile, "rb") as f:
    masked_covariance = pickle.load(f)

outfile = "/home/jack/Documents/data/binned_masked_cov.pkl"
with open(outfile, "rb") as f:
    binned_masked_covariance = pickle.load(f)

noise_level = 10.0
noise_level *= np.pi / (180.0 * 60.0)
ell = np.arange(lmax + 1)
noise_spectra = ell * (ell + 1) * noise_level**2 / (2 * np.pi)
noise_dict = {"ell": ell, "bb": noise_spectra}

r = 0.0
nt = 0.0
pivot_t = 0.01
keys = ["bb"]

planck_path = "/home/jack/cobaya/code/CAMB/inifiles/planck_2018.ini"
pars = camb.read_ini(planck_path)

pars.InitPower.set_params(
    As=2.100549e-9,
    ns=0.9660499,
    r=r,
    nt=nt,
    pivot_tensor=pivot_t,
    pivot_scalar=0.05,
    parameterization=2,
)
pars.WantTensors = True
pars.Accuracy.AccurateBB = True
pars.DoLensing = True

results = camb.get_results(pars)
res = results.get_cmb_power_spectra(
    CMB_unit="muK",
    lmax=lmax,
    raw_cl=False,
)
CLS = CAMBres2dict(res, keys)

# bins = np.arange(0, lmax + 1, 5)
# digitized = np.digitize(ell, bins)
# bin_means = [ell[digitized == i].mean() for i in range(1, len(bins))]
# bb_means = [CLS["bb"][digitized == i].mean() for i in range(1, len(bins))]

# print(np.array(bin_means), np.array(bb_means))
# plt.plot(ell, CLS["bb"], label="original")
# plt.plot(bin_means, bb_means, label="binned")
# plt.show()
# plt.loglog()
# exit()

exactBB = LiLit(
    name=name,
    fields="b",
    # like="exact",
    # like="gaussian",
    like="correlated_gaussian",
    cl_file=CLS,
    nl_file=noise_dict,
    # r=r,
    # nt=nt,
    external_covariance=masked_covariance,
    # experiment="PTEPLiteBIRD",
    # nside=128,
    debug=debug,
    lmin=2,
    lmax=lmax,
    fsky=0.6,
)

# gaussBB = LiLit(
#     name=name,
#     fields="b",
#     like="gaussian",
#     r=r,
#     nt=nt,
#     experiment="PTEPLiteBIRD",
#     nside=128,
#     debug=debug,
#     lmin=2,
#     lmax=lmax,
#     fsky=0.60,
# )

info = {
    "likelihood": {name: exactBB},
    "params": {
        "As": 2.100549e-9,
        "ns": 0.9660499,
        "ombh2": 0.0223828,
        "omch2": 0.1201075,
        "omnuh2": 0.6451439e-03,
        "H0": 67.32117,
        "tau": 0.05430842,
        # "nt": {
        #     "latex": "n_t",
        #     "prior": {"max": 5, "min": -5},
        #     "proposal": 0.1,
        #     # "ref": {"dist": "norm", "loc": nt, "scale": 0.001},
        #     "ref": 0.0,
        # },
        "r": {
            "latex": "r_{0.01}",
            "prior": {"max": 3, "min": 1e-5},
            "proposal": 0.0005,
            # "ref": {"dist": "norm", "loc": r, "scale": 0.0001},
            "ref": 0.0001,
        },
        # "r005": {
        #     "derived": "lambda r, nt, ns: r * (0.05/0.01)**(nt - ns + 1)",
        #     "min": 0,
        #     "max": 3,
        #     "latex": "r_{0.05}",
        # },
    },
    "output": f"chains/masked2{name}_lmax{lmax}",
    "force": True,
    # "resume": True,
    # "debug": True,
    "stop-at-error": True,
    "sampler": {
        "mcmc": {
            "Rminus1_cl_stop": 0.2,
            "Rminus1_stop": 0.01,
        },
    },
    "theory": {
        "camb": {
            "extra_args": {
                "bbn_predictor": "PArthENoPE_880.2_standard.dat",
                "halofit_version": "mead",
                "lens_potential_accuracy": 1,
                "NonLinear": "NonLinear_both",  # This is necessary to be concordant with Planck2018 fiducial spectra
                "max_l": 2700,  # This is necessary to get accurate lensing B-modes
                "WantTransfer": True,  # This is necessary to be concordant with Planck2018 fiducial spectra
                "Transfer.high_precision": True,  # This is necessary to be concordant with Planck2018 fiducial spectra (this will impact negatively on the performance, so you might want to switch it off. However, remember to chanfe the fiducial accordingly.)
                "parameterization": 2,
                "num_nu_massless": 2.046,
                "share_delta_neff": True,
                "YHe": 0.2454006,
                "pivot_tensor": 0.05,
                "num_massive_neutrinos": 1,
                "theta_H0_range": [20, 100],
            },
        },
    },
}

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

start = time.time()

success = False
try:
    upd_info, mcmc = run(info)
    success = True
except LoggedError as err:
    print(err)

success = all(comm.allgather(success))

if not success and rank == 0:
    print("Sampling failed!")

end = time.time()

print(f"******** ALL DONE IN {round(end-start, 2)} SECONDS! ********")
