import cProfile

# noinspection PyUnresolvedReferences
import jaba_speedup
from main import *

with cProfile.Profile() as pr:
    try:
        main()
    finally:
        pr.dump_stats("./main.profile")
