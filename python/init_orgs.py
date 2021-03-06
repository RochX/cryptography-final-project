import os
from main import CLA, CTF

CLA = CLA()
CTF = CTF()

# reset voting data
CLA.saveVoters(True)
CTF.saveVoteTally(True)

# storing variables in files relies on a folder called 'variable_files' existing first
if not os.path.exists('variable_files'):
    os.mkdir('variable_files')

# save initial state
CLA.saveIDListToFile()
CLA.saveAuthDictToFile()
CTF.saveIDListToFile()
