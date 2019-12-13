# Useful toolkits for operation using openbabel
from subprocess import run
from pathlib import Path

cmd = "obabel"

default_params = {"3D": {"-ismi": "",
                         "--gen3D": "",
                         "--fastest": "",
                         "--log": "",
                         "-O": "3D.xyz"},
                  "conformer": {"--conformer": "",
                                "--writeconformers": "",
                                "--nconf": 5,
                                "--log": "",
                                "--convergence": 25,
                                "-O": "conformer.xyz"},
                  "mm": {"--minimize": "",
                         "--log": "",
                         "--ff": "GAFF",
                         "--crit": 1e-5,
                         "--steps": 10,
                         "-l": 3,
                         "-O": "mm.xyz",},
}


def _compile_job_string(params):
    params.pop("-O")
    args = []
    for k, v in params.items():
        if v in (None, ""):
            args.append(str(k))
        else:
            args += [str(k), str(v)]
    return args


def run_job(job, infile, outfile=None,  **kwargs):
    """Convert infile to outfile using obabel
    `job can be `3D`, `conformer` `mm`
    `kwargs are extra key:val pair to overwrite default parameters
    """
    # If babel exists?
    if run("which {0}".format(cmd), shell=True).returncode != 0:
        raise RuntimeError("Openbabel binary not found!")

    if job not in default_params.keys():
        raise KeyError("Job type unknown!")

    params = default_params[job]
    params.update(**kwargs)
    if outfile is not None:
        outfile = Path(outfile).resolve().as_posix()
    else:
        outfile = Path(infile).parent / params["-O"]
    params.update(**{"-O": outfile})
        
        
    args = [cmd, "{0}".format(Path(infile).resolve()),
            "-O", "{0}".format(params["-O"])]
    args += _compile_job_string(params)
    # print(args, "")
    log = Path(outfile).parent / "{0}.log".format(job)
    job_string = " ".join(args)
    print(job_string)
    with open(log, "w") as f:
        proc = run(job_string,
                  shell=True,
                  stdout=f, stderr=f)
    ec = proc.returncode
    if ec == 0:
        print("Job {0} finished successfully.".format(job))
    else:
        print("Job {0} failed. Please check log for details".format(job))
    return ec
        

if __name__ == '__main__':
    import sys
    infile = sys.argv[1]
    outfile = sys.argv[2]
    job = sys.argv[3]
    run_job(job, infile, outfile)
