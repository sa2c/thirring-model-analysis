fort100cols = [
    'real_psibarpsi1', 'aimag_psibarpsi1', 'real_psibarpsi2',
    'aimag_psibarpsi2'
]
fort200cols = ["psibarpsi", "susclsing"]
fort11cols = ['isweep', 'gaction', 'paction']

cols = {'fort.100':fort100cols, 'fort.200' : fort200cols, 'fort.11' : fort11cols}

fort100cols_newcode = [
    'isweep_total',
    'real_psibarpsi1', 'aimag_psibarpsi1', 'real_psibarpsi2',
    'aimag_psibarpsi2'
]

cols_new = {'fort.100':fort100cols_newcode, 'fort.200' : fort200cols, 'fort.11' : fort11cols}
