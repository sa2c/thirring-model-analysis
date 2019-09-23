SHELL = bash

all:  ./cond_m01_Ls32_L12 ./cond_m01_Ls32_L16 ./cond_m01_Ls40_L12 ./cond_m01_Ls40_L16\
 ./cond_m01_Ls48_L12 ./cond_m01_Ls48_L16 ./cond_m01_LsINF_L12 ./cond_m01_LsINF_L16\
 ./cond_m02_Ls32_L12 ./cond_m02_Ls32_L16 ./cond_m02_Ls40_L12 ./cond_m02_Ls40_L16\
 ./cond_m02_Ls48_L12 ./cond_m02_Ls48_L16 ./cond_m02_LsINF_L12 ./cond_m02_LsINF_L16\
 ./cond_m03_Ls32_L12 ./cond_m03_Ls32_L16 ./cond_m03_Ls40_L12 ./cond_m03_Ls40_L16\
 ./cond_m03_Ls48_L12 ./cond_m03_Ls48_L16 ./cond_m03_LsINF_L12 ./cond_m03_LsINF_L16\
 ./cond_m04_Ls32_L12 ./cond_m04_Ls32_L16 ./cond_m04_Ls40_L12 ./cond_m04_Ls40_L16\
 ./cond_m04_Ls48_L12 ./cond_m04_Ls48_L16 ./cond_m04_LsINF_L12 ./cond_m04_LsINF_L16\
 ./cond_m05_Ls32_L12 ./cond_m05_Ls32_L16 ./cond_m05_Ls40_L12 ./cond_m05_Ls40_L16\
 ./cond_m05_Ls48_L12 ./cond_m05_Ls48_L16 ./cond_m05_LsINF_L12 ./cond_m05_LsINF_L16\
 ./fitLs32L12.png ./fitLs32L16.png ./fitLs40L12.png ./fitLs40L16.png ./fitLs48L12.png\
 ./fitLs48L16.png ./fitLsinfL12.png ./fitLsinfL16.png ./pbpextrL12_m0.01.png\
 ./pbpextrL12_m0.02.png ./pbpextrL12_m0.03.png ./pbpextrL12_m0.04.png ./pbpextrL12_m0.05.png\
 ./pbpextrL16_m0.01.png ./pbpextrL16_m0.02.png ./pbpextrL16_m0.03.png ./pbpextrL16_m0.04.png\
 ./pbpextrL16_m0.05.png ./psibarpsi.csv ./psibarpsi.pretty.csv ./psibarpsi_extrapolated.csv\
 ./psibarpsi_extrapolated_pretty.csv

 ./cond_m01_LsINF_L16 ./cond_m02_LsINF_L16 ./cond_m03_LsINF_L16 ./cond_m04_LsINF_L16\
 ./cond_m05_LsINF_L16 ./fitLsinfL16.png :  ./psibarpsi_extrapolated.csv
	. ../Scripts/lib.sh&&cd .&&../ProtocolUtils/log ../Scripts/eos_fit_inf.py 16 --savefig

 ./cond_m01_LsINF_L12 ./cond_m02_LsINF_L12 ./cond_m03_LsINF_L12 ./cond_m04_LsINF_L12\
 ./cond_m05_LsINF_L12 ./fitLsinfL12.png :  ./psibarpsi_extrapolated.csv
	. ../Scripts/lib.sh&&cd .&&../ProtocolUtils/log ../Scripts/eos_fit_inf.py 12 --savefig

 ./cond_m01_Ls32_L16 ./cond_m02_Ls32_L16 ./cond_m03_Ls32_L16 ./cond_m04_Ls32_L16\
 ./cond_m05_Ls32_L16 ./fitLs32L16.png :  ./psibarpsi.csv
	. ../Scripts/lib.sh&&cd .&&../ProtocolUtils/log ../Scripts/eos_fit_v2.py 32 16 --savefig

 ./cond_m01_Ls32_L12 ./cond_m02_Ls32_L12 ./cond_m03_Ls32_L12 ./cond_m04_Ls32_L12\
 ./cond_m05_Ls32_L12 ./fitLs32L12.png :  ./psibarpsi.csv
	. ../Scripts/lib.sh&&cd .&&../ProtocolUtils/log ../Scripts/eos_fit_v2.py 32 12 --savefig

 ./cond_m01_Ls40_L12 ./cond_m02_Ls40_L12 ./cond_m03_Ls40_L12 ./cond_m04_Ls40_L12\
 ./cond_m05_Ls40_L12 ./fitLs40L12.png :  ./psibarpsi.csv
	. ../Scripts/lib.sh&&cd .&&../ProtocolUtils/log ../Scripts/eos_fit_v2.py 40 12 --savefig

 ./cond_m01_Ls48_L16 ./cond_m02_Ls48_L16 ./cond_m03_Ls48_L16 ./cond_m04_Ls48_L16\
 ./cond_m05_Ls48_L16 ./fitLs48L16.png :  ./psibarpsi.csv
	. ../Scripts/lib.sh&&cd .&&../ProtocolUtils/log ../Scripts/eos_fit_v2.py 48 16 --savefig

 ./cond_m01_Ls48_L12 ./cond_m02_Ls48_L12 ./cond_m03_Ls48_L12 ./cond_m04_Ls48_L12\
 ./cond_m05_Ls48_L12 ./fitLs48L12.png :  ./psibarpsi.csv
	. ../Scripts/lib.sh&&cd .&&../ProtocolUtils/log ../Scripts/eos_fit_v2.py 48 12 --savefig

 ./cond_m01_Ls40_L16 ./cond_m02_Ls40_L16 ./cond_m03_Ls40_L16 ./cond_m04_Ls40_L16\
 ./cond_m05_Ls40_L16 ./fitLs40L16.png :  ./psibarpsi.csv
	. ../Scripts/lib.sh&&cd .&&../ProtocolUtils/log ../Scripts/eos_fit_v2.py 40 16 --savefig

 ./pbpextrL12_m0.01.png ./pbpextrL12_m0.02.png ./pbpextrL12_m0.03.png ./pbpextrL12_m0.04.png\
 ./pbpextrL12_m0.05.png ./pbpextrL16_m0.01.png ./pbpextrL16_m0.02.png ./pbpextrL16_m0.03.png\
 ./pbpextrL16_m0.04.png ./pbpextrL16_m0.05.png ./psibarpsi_extrapolated.csv\
 ./psibarpsi_extrapolated_pretty.csv :  ./psibarpsi.csv
	. ../Scripts/lib.sh&&cd .&&../ProtocolUtils/log ../Scripts/extrapolate_to_linf.py

 ./psibarpsi.csv ./psibarpsi.pretty.csv :  ./all_dirs/Ls32.beta0.30.m0.01/fort.200.total.1.csv\
 ./all_dirs/Ls32.beta0.30.m0.01/fort.200.total.2.csv\
 ./all_dirs/Ls32.beta0.30.m0.02/fort.200.total.1.csv\
 ./all_dirs/Ls32.beta0.30.m0.02/fort.200.total.2.csv\
 ./all_dirs/Ls32.beta0.30.m0.03/fort.200.total.1.csv\
 ./all_dirs/Ls32.beta0.30.m0.03/fort.200.total.2.csv\
 ./all_dirs/Ls32.beta0.30.m0.04/fort.200.total.1.csv\
 ./all_dirs/Ls32.beta0.30.m0.04/fort.200.total.2.csv\
 ./all_dirs/Ls32.beta0.30.m0.05/fort.200.total.1.csv\
 ./all_dirs/Ls32.beta0.30.m0.05/fort.200.total.2.csv\
 ./all_dirs/Ls32.beta0.32.m0.01/fort.200.total.1.csv\
 ./all_dirs/Ls32.beta0.32.m0.01/fort.200.total.2.csv\
 ./all_dirs/Ls32.beta0.32.m0.02/fort.200.total.1.csv\
 ./all_dirs/Ls32.beta0.32.m0.02/fort.200.total.2.csv\
 ./all_dirs/Ls32.beta0.32.m0.03/fort.200.total.1.csv\
 ./all_dirs/Ls32.beta0.32.m0.03/fort.200.total.2.csv\
 ./all_dirs/Ls32.beta0.32.m0.04/fort.200.total.1.csv\
 ./all_dirs/Ls32.beta0.32.m0.04/fort.200.total.2.csv\
 ./all_dirs/Ls32.beta0.32.m0.05/fort.200.total.1.csv\
 ./all_dirs/Ls32.beta0.32.m0.05/fort.200.total.2.csv\
 ./all_dirs/Ls32.beta0.34.m0.01/fort.200.total.1.csv\
 ./all_dirs/Ls32.beta0.34.m0.01/fort.200.total.2.csv\
 ./all_dirs/Ls32.beta0.34.m0.02/fort.200.total.1.csv\
 ./all_dirs/Ls32.beta0.34.m0.02/fort.200.total.2.csv\
 ./all_dirs/Ls32.beta0.34.m0.03/fort.200.total.1.csv\
 ./all_dirs/Ls32.beta0.34.m0.03/fort.200.total.2.csv\
 ./all_dirs/Ls32.beta0.34.m0.04/fort.200.total.1.csv\
 ./all_dirs/Ls32.beta0.34.m0.04/fort.200.total.2.csv\
 ./all_dirs/Ls32.beta0.34.m0.05/fort.200.total.1.csv\
 ./all_dirs/Ls32.beta0.34.m0.05/fort.200.total.2.csv\
 ./all_dirs/Ls32.beta0.36.m0.01/fort.200.total.1.csv\
 ./all_dirs/Ls32.beta0.36.m0.01/fort.200.total.2.csv\
 ./all_dirs/Ls32.beta0.36.m0.02/fort.200.total.1.csv\
 ./all_dirs/Ls32.beta0.36.m0.02/fort.200.total.2.csv\
 ./all_dirs/Ls32.beta0.36.m0.03/fort.200.total.1.csv\
 ./all_dirs/Ls32.beta0.36.m0.03/fort.200.total.2.csv\
 ./all_dirs/Ls32.beta0.36.m0.04/fort.200.total.1.csv\
 ./all_dirs/Ls32.beta0.36.m0.04/fort.200.total.2.csv\
 ./all_dirs/Ls32.beta0.36.m0.05/fort.200.total.1.csv\
 ./all_dirs/Ls32.beta0.36.m0.05/fort.200.total.2.csv\
 ./all_dirs/Ls32.beta0.38.m0.01/fort.200.total.1.csv\
 ./all_dirs/Ls32.beta0.38.m0.01/fort.200.total.2.csv\
 ./all_dirs/Ls32.beta0.38.m0.02/fort.200.total.1.csv\
 ./all_dirs/Ls32.beta0.38.m0.02/fort.200.total.2.csv\
 ./all_dirs/Ls32.beta0.38.m0.03/fort.200.total.1.csv\
 ./all_dirs/Ls32.beta0.38.m0.03/fort.200.total.2.csv\
 ./all_dirs/Ls32.beta0.38.m0.04/fort.200.total.1.csv\
 ./all_dirs/Ls32.beta0.38.m0.04/fort.200.total.2.csv\
 ./all_dirs/Ls32.beta0.38.m0.05/fort.200.total.1.csv\
 ./all_dirs/Ls32.beta0.38.m0.05/fort.200.total.2.csv\
 ./all_dirs/Ls32.beta0.40.m0.01/fort.200.total.1.csv\
 ./all_dirs/Ls32.beta0.40.m0.01/fort.200.total.2.csv\
 ./all_dirs/Ls32.beta0.40.m0.02/fort.200.total.1.csv\
 ./all_dirs/Ls32.beta0.40.m0.02/fort.200.total.2.csv\
 ./all_dirs/Ls32.beta0.40.m0.03/fort.200.total.1.csv\
 ./all_dirs/Ls32.beta0.40.m0.03/fort.200.total.2.csv\
 ./all_dirs/Ls32.beta0.40.m0.04/fort.200.total.1.csv\
 ./all_dirs/Ls32.beta0.40.m0.04/fort.200.total.2.csv\
 ./all_dirs/Ls32.beta0.40.m0.05/fort.200.total.1.csv\
 ./all_dirs/Ls32.beta0.40.m0.05/fort.200.total.2.csv\
 ./all_dirs/Ls32.beta0.42.m0.01/fort.200.total.1.csv\
 ./all_dirs/Ls32.beta0.42.m0.01/fort.200.total.2.csv\
 ./all_dirs/Ls32.beta0.42.m0.02/fort.200.total.1.csv\
 ./all_dirs/Ls32.beta0.42.m0.02/fort.200.total.2.csv\
 ./all_dirs/Ls32.beta0.42.m0.03/fort.200.total.1.csv\
 ./all_dirs/Ls32.beta0.42.m0.03/fort.200.total.2.csv\
 ./all_dirs/Ls32.beta0.42.m0.04/fort.200.total.1.csv\
 ./all_dirs/Ls32.beta0.42.m0.04/fort.200.total.2.csv\
 ./all_dirs/Ls32.beta0.42.m0.05/fort.200.total.1.csv\
 ./all_dirs/Ls32.beta0.42.m0.05/fort.200.total.2.csv\
 ./all_dirs/Ls32.beta0.44.m0.01/fort.200.total.1.csv\
 ./all_dirs/Ls32.beta0.44.m0.01/fort.200.total.2.csv\
 ./all_dirs/Ls32.beta0.44.m0.02/fort.200.total.1.csv\
 ./all_dirs/Ls32.beta0.44.m0.02/fort.200.total.2.csv\
 ./all_dirs/Ls32.beta0.44.m0.03/fort.200.total.1.csv\
 ./all_dirs/Ls32.beta0.44.m0.03/fort.200.total.2.csv\
 ./all_dirs/Ls32.beta0.44.m0.04/fort.200.total.1.csv\
 ./all_dirs/Ls32.beta0.44.m0.04/fort.200.total.2.csv\
 ./all_dirs/Ls32.beta0.44.m0.05/fort.200.total.1.csv\
 ./all_dirs/Ls32.beta0.44.m0.05/fort.200.total.2.csv\
 ./all_dirs/Ls32.beta0.46.m0.01/fort.200.total.1.csv\
 ./all_dirs/Ls32.beta0.46.m0.01/fort.200.total.2.csv\
 ./all_dirs/Ls32.beta0.46.m0.02/fort.200.total.1.csv\
 ./all_dirs/Ls32.beta0.46.m0.02/fort.200.total.2.csv\
 ./all_dirs/Ls32.beta0.46.m0.03/fort.200.total.1.csv\
 ./all_dirs/Ls32.beta0.46.m0.03/fort.200.total.2.csv\
 ./all_dirs/Ls32.beta0.46.m0.04/fort.200.total.1.csv\
 ./all_dirs/Ls32.beta0.46.m0.04/fort.200.total.2.csv\
 ./all_dirs/Ls32.beta0.46.m0.05/fort.200.total.1.csv\
 ./all_dirs/Ls32.beta0.46.m0.05/fort.200.total.2.csv\
 ./all_dirs/Ls32.beta0.55.m0.01/fort.200.total.1.csv\
 ./all_dirs/Ls32.beta0.55.m0.01/fort.200.total.2.csv\
 ./all_dirs/Ls32.beta0.55.m0.02/fort.200.total.1.csv\
 ./all_dirs/Ls32.beta0.55.m0.02/fort.200.total.2.csv\
 ./all_dirs/Ls32.beta0.55.m0.03/fort.200.total.1.csv\
 ./all_dirs/Ls32.beta0.55.m0.03/fort.200.total.2.csv\
 ./all_dirs/Ls32.beta0.55.m0.04/fort.200.total.1.csv\
 ./all_dirs/Ls32.beta0.55.m0.04/fort.200.total.2.csv\
 ./all_dirs/Ls32.beta0.55.m0.05/fort.200.total.1.csv\
 ./all_dirs/Ls32.beta0.55.m0.05/fort.200.total.2.csv\
 ./all_dirs/Ls40.beta0.30.m0.01/fort.200.total.1.csv\
 ./all_dirs/Ls40.beta0.30.m0.01/fort.200.total.2.csv\
 ./all_dirs/Ls40.beta0.30.m0.02/fort.200.total.1.csv\
 ./all_dirs/Ls40.beta0.30.m0.02/fort.200.total.2.csv\
 ./all_dirs/Ls40.beta0.30.m0.03/fort.200.total.1.csv\
 ./all_dirs/Ls40.beta0.30.m0.03/fort.200.total.2.csv\
 ./all_dirs/Ls40.beta0.30.m0.04/fort.200.total.1.csv\
 ./all_dirs/Ls40.beta0.30.m0.04/fort.200.total.2.csv\
 ./all_dirs/Ls40.beta0.30.m0.05/fort.200.total.1.csv\
 ./all_dirs/Ls40.beta0.30.m0.05/fort.200.total.2.csv\
 ./all_dirs/Ls40.beta0.32.m0.01/fort.200.total.1.csv\
 ./all_dirs/Ls40.beta0.32.m0.01/fort.200.total.2.csv\
 ./all_dirs/Ls40.beta0.32.m0.02/fort.200.total.1.csv\
 ./all_dirs/Ls40.beta0.32.m0.02/fort.200.total.2.csv\
 ./all_dirs/Ls40.beta0.32.m0.03/fort.200.total.1.csv\
 ./all_dirs/Ls40.beta0.32.m0.03/fort.200.total.2.csv\
 ./all_dirs/Ls40.beta0.32.m0.04/fort.200.total.1.csv\
 ./all_dirs/Ls40.beta0.32.m0.04/fort.200.total.2.csv\
 ./all_dirs/Ls40.beta0.32.m0.05/fort.200.total.1.csv\
 ./all_dirs/Ls40.beta0.32.m0.05/fort.200.total.2.csv\
 ./all_dirs/Ls40.beta0.34.m0.01/fort.200.total.1.csv\
 ./all_dirs/Ls40.beta0.34.m0.01/fort.200.total.2.csv\
 ./all_dirs/Ls40.beta0.34.m0.02/fort.200.total.1.csv\
 ./all_dirs/Ls40.beta0.34.m0.02/fort.200.total.2.csv\
 ./all_dirs/Ls40.beta0.34.m0.03/fort.200.total.1.csv\
 ./all_dirs/Ls40.beta0.34.m0.03/fort.200.total.2.csv\
 ./all_dirs/Ls40.beta0.34.m0.04/fort.200.total.1.csv\
 ./all_dirs/Ls40.beta0.34.m0.04/fort.200.total.2.csv\
 ./all_dirs/Ls40.beta0.34.m0.05/fort.200.total.1.csv\
 ./all_dirs/Ls40.beta0.34.m0.05/fort.200.total.2.csv\
 ./all_dirs/Ls40.beta0.36.m0.01/fort.200.total.1.csv\
 ./all_dirs/Ls40.beta0.36.m0.01/fort.200.total.2.csv\
 ./all_dirs/Ls40.beta0.36.m0.02/fort.200.total.1.csv\
 ./all_dirs/Ls40.beta0.36.m0.02/fort.200.total.2.csv\
 ./all_dirs/Ls40.beta0.36.m0.03/fort.200.total.1.csv\
 ./all_dirs/Ls40.beta0.36.m0.03/fort.200.total.2.csv\
 ./all_dirs/Ls40.beta0.36.m0.04/fort.200.total.1.csv\
 ./all_dirs/Ls40.beta0.36.m0.04/fort.200.total.2.csv\
 ./all_dirs/Ls40.beta0.36.m0.05/fort.200.total.1.csv\
 ./all_dirs/Ls40.beta0.36.m0.05/fort.200.total.2.csv\
 ./all_dirs/Ls40.beta0.38.m0.01/fort.200.total.1.csv\
 ./all_dirs/Ls40.beta0.38.m0.01/fort.200.total.2.csv\
 ./all_dirs/Ls40.beta0.38.m0.02/fort.200.total.1.csv\
 ./all_dirs/Ls40.beta0.38.m0.02/fort.200.total.2.csv\
 ./all_dirs/Ls40.beta0.38.m0.03/fort.200.total.1.csv\
 ./all_dirs/Ls40.beta0.38.m0.03/fort.200.total.2.csv\
 ./all_dirs/Ls40.beta0.38.m0.04/fort.200.total.1.csv\
 ./all_dirs/Ls40.beta0.38.m0.04/fort.200.total.2.csv\
 ./all_dirs/Ls40.beta0.38.m0.05/fort.200.total.1.csv\
 ./all_dirs/Ls40.beta0.38.m0.05/fort.200.total.2.csv\
 ./all_dirs/Ls40.beta0.40.m0.01/fort.200.total.1.csv\
 ./all_dirs/Ls40.beta0.40.m0.01/fort.200.total.2.csv\
 ./all_dirs/Ls40.beta0.40.m0.02/fort.200.total.1.csv\
 ./all_dirs/Ls40.beta0.40.m0.02/fort.200.total.2.csv\
 ./all_dirs/Ls40.beta0.40.m0.03/fort.200.total.1.csv\
 ./all_dirs/Ls40.beta0.40.m0.03/fort.200.total.2.csv\
 ./all_dirs/Ls40.beta0.40.m0.04/fort.200.total.1.csv\
 ./all_dirs/Ls40.beta0.40.m0.04/fort.200.total.2.csv\
 ./all_dirs/Ls40.beta0.40.m0.05/fort.200.total.1.csv\
 ./all_dirs/Ls40.beta0.40.m0.05/fort.200.total.2.csv\
 ./all_dirs/Ls40.beta0.42.m0.01/fort.200.total.1.csv\
 ./all_dirs/Ls40.beta0.42.m0.01/fort.200.total.2.csv\
 ./all_dirs/Ls40.beta0.42.m0.02/fort.200.total.1.csv\
 ./all_dirs/Ls40.beta0.42.m0.02/fort.200.total.2.csv\
 ./all_dirs/Ls40.beta0.42.m0.03/fort.200.total.1.csv\
 ./all_dirs/Ls40.beta0.42.m0.03/fort.200.total.2.csv\
 ./all_dirs/Ls40.beta0.42.m0.04/fort.200.total.1.csv\
 ./all_dirs/Ls40.beta0.42.m0.04/fort.200.total.2.csv\
 ./all_dirs/Ls40.beta0.42.m0.05/fort.200.total.1.csv\
 ./all_dirs/Ls40.beta0.42.m0.05/fort.200.total.2.csv\
 ./all_dirs/Ls40.beta0.44.m0.01/fort.200.total.1.csv\
 ./all_dirs/Ls40.beta0.44.m0.01/fort.200.total.2.csv\
 ./all_dirs/Ls40.beta0.44.m0.02/fort.200.total.1.csv\
 ./all_dirs/Ls40.beta0.44.m0.02/fort.200.total.2.csv\
 ./all_dirs/Ls40.beta0.44.m0.03/fort.200.total.1.csv\
 ./all_dirs/Ls40.beta0.44.m0.03/fort.200.total.2.csv\
 ./all_dirs/Ls40.beta0.44.m0.04/fort.200.total.1.csv\
 ./all_dirs/Ls40.beta0.44.m0.04/fort.200.total.2.csv\
 ./all_dirs/Ls40.beta0.44.m0.05/fort.200.total.1.csv\
 ./all_dirs/Ls40.beta0.44.m0.05/fort.200.total.2.csv\
 ./all_dirs/Ls40.beta0.46.m0.01/fort.200.total.1.csv\
 ./all_dirs/Ls40.beta0.46.m0.01/fort.200.total.2.csv\
 ./all_dirs/Ls40.beta0.46.m0.02/fort.200.total.1.csv\
 ./all_dirs/Ls40.beta0.46.m0.02/fort.200.total.2.csv\
 ./all_dirs/Ls40.beta0.46.m0.03/fort.200.total.1.csv\
 ./all_dirs/Ls40.beta0.46.m0.03/fort.200.total.2.csv\
 ./all_dirs/Ls40.beta0.46.m0.04/fort.200.total.1.csv\
 ./all_dirs/Ls40.beta0.46.m0.04/fort.200.total.2.csv\
 ./all_dirs/Ls40.beta0.46.m0.05/fort.200.total.1.csv\
 ./all_dirs/Ls40.beta0.46.m0.05/fort.200.total.2.csv\
 ./all_dirs/Ls40.beta0.55.m0.01/fort.200.total.1.csv\
 ./all_dirs/Ls40.beta0.55.m0.01/fort.200.total.2.csv\
 ./all_dirs/Ls40.beta0.55.m0.02/fort.200.total.1.csv\
 ./all_dirs/Ls40.beta0.55.m0.02/fort.200.total.2.csv\
 ./all_dirs/Ls40.beta0.55.m0.03/fort.200.total.1.csv\
 ./all_dirs/Ls40.beta0.55.m0.03/fort.200.total.2.csv\
 ./all_dirs/Ls40.beta0.55.m0.04/fort.200.total.1.csv\
 ./all_dirs/Ls40.beta0.55.m0.04/fort.200.total.2.csv\
 ./all_dirs/Ls40.beta0.55.m0.05/fort.200.total.1.csv\
 ./all_dirs/Ls40.beta0.55.m0.05/fort.200.total.2.csv\
 ./all_dirs/Ls48.beta0.30.m0.01/fort.200.total.1.csv\
 ./all_dirs/Ls48.beta0.30.m0.01/fort.200.total.2.csv\
 ./all_dirs/Ls48.beta0.30.m0.02/fort.200.total.1.csv\
 ./all_dirs/Ls48.beta0.30.m0.02/fort.200.total.2.csv\
 ./all_dirs/Ls48.beta0.30.m0.03/fort.200.total.1.csv\
 ./all_dirs/Ls48.beta0.30.m0.03/fort.200.total.2.csv\
 ./all_dirs/Ls48.beta0.30.m0.04/fort.200.total.1.csv\
 ./all_dirs/Ls48.beta0.30.m0.04/fort.200.total.2.csv\
 ./all_dirs/Ls48.beta0.30.m0.05/fort.200.total.1.csv\
 ./all_dirs/Ls48.beta0.30.m0.05/fort.200.total.2.csv\
 ./all_dirs/Ls48.beta0.32.m0.01/fort.200.total.1.csv\
 ./all_dirs/Ls48.beta0.32.m0.01/fort.200.total.2.csv\
 ./all_dirs/Ls48.beta0.32.m0.02/fort.200.total.1.csv\
 ./all_dirs/Ls48.beta0.32.m0.02/fort.200.total.2.csv\
 ./all_dirs/Ls48.beta0.32.m0.03/fort.200.total.1.csv\
 ./all_dirs/Ls48.beta0.32.m0.03/fort.200.total.2.csv\
 ./all_dirs/Ls48.beta0.32.m0.04/fort.200.total.1.csv\
 ./all_dirs/Ls48.beta0.32.m0.04/fort.200.total.2.csv\
 ./all_dirs/Ls48.beta0.32.m0.05/fort.200.total.1.csv\
 ./all_dirs/Ls48.beta0.32.m0.05/fort.200.total.2.csv\
 ./all_dirs/Ls48.beta0.34.m0.01/fort.200.total.1.csv\
 ./all_dirs/Ls48.beta0.34.m0.01/fort.200.total.2.csv\
 ./all_dirs/Ls48.beta0.34.m0.02/fort.200.total.1.csv\
 ./all_dirs/Ls48.beta0.34.m0.02/fort.200.total.2.csv\
 ./all_dirs/Ls48.beta0.34.m0.03/fort.200.total.1.csv\
 ./all_dirs/Ls48.beta0.34.m0.03/fort.200.total.2.csv\
 ./all_dirs/Ls48.beta0.34.m0.04/fort.200.total.1.csv\
 ./all_dirs/Ls48.beta0.34.m0.04/fort.200.total.2.csv\
 ./all_dirs/Ls48.beta0.34.m0.05/fort.200.total.1.csv\
 ./all_dirs/Ls48.beta0.34.m0.05/fort.200.total.2.csv\
 ./all_dirs/Ls48.beta0.36.m0.01/fort.200.total.1.csv\
 ./all_dirs/Ls48.beta0.36.m0.01/fort.200.total.2.csv\
 ./all_dirs/Ls48.beta0.36.m0.02/fort.200.total.1.csv\
 ./all_dirs/Ls48.beta0.36.m0.02/fort.200.total.2.csv\
 ./all_dirs/Ls48.beta0.36.m0.03/fort.200.total.1.csv\
 ./all_dirs/Ls48.beta0.36.m0.03/fort.200.total.2.csv\
 ./all_dirs/Ls48.beta0.36.m0.04/fort.200.total.1.csv\
 ./all_dirs/Ls48.beta0.36.m0.04/fort.200.total.2.csv\
 ./all_dirs/Ls48.beta0.36.m0.05/fort.200.total.1.csv\
 ./all_dirs/Ls48.beta0.36.m0.05/fort.200.total.2.csv\
 ./all_dirs/Ls48.beta0.38.m0.01/fort.200.total.1.csv\
 ./all_dirs/Ls48.beta0.38.m0.01/fort.200.total.2.csv\
 ./all_dirs/Ls48.beta0.38.m0.02/fort.200.total.1.csv\
 ./all_dirs/Ls48.beta0.38.m0.02/fort.200.total.2.csv\
 ./all_dirs/Ls48.beta0.38.m0.03/fort.200.total.1.csv\
 ./all_dirs/Ls48.beta0.38.m0.03/fort.200.total.2.csv\
 ./all_dirs/Ls48.beta0.38.m0.04/fort.200.total.1.csv\
 ./all_dirs/Ls48.beta0.38.m0.04/fort.200.total.2.csv\
 ./all_dirs/Ls48.beta0.38.m0.05/fort.200.total.1.csv\
 ./all_dirs/Ls48.beta0.38.m0.05/fort.200.total.2.csv\
 ./all_dirs/Ls48.beta0.40.m0.01/fort.200.total.1.csv\
 ./all_dirs/Ls48.beta0.40.m0.01/fort.200.total.2.csv\
 ./all_dirs/Ls48.beta0.40.m0.02/fort.200.total.1.csv\
 ./all_dirs/Ls48.beta0.40.m0.02/fort.200.total.2.csv\
 ./all_dirs/Ls48.beta0.40.m0.03/fort.200.total.1.csv\
 ./all_dirs/Ls48.beta0.40.m0.03/fort.200.total.2.csv\
 ./all_dirs/Ls48.beta0.40.m0.04/fort.200.total.1.csv\
 ./all_dirs/Ls48.beta0.40.m0.04/fort.200.total.2.csv\
 ./all_dirs/Ls48.beta0.40.m0.05/fort.200.total.1.csv\
 ./all_dirs/Ls48.beta0.40.m0.05/fort.200.total.2.csv\
 ./all_dirs/Ls48.beta0.42.m0.01/fort.200.total.1.csv\
 ./all_dirs/Ls48.beta0.42.m0.01/fort.200.total.2.csv\
 ./all_dirs/Ls48.beta0.42.m0.02/fort.200.total.1.csv\
 ./all_dirs/Ls48.beta0.42.m0.02/fort.200.total.2.csv\
 ./all_dirs/Ls48.beta0.42.m0.03/fort.200.total.1.csv\
 ./all_dirs/Ls48.beta0.42.m0.03/fort.200.total.2.csv\
 ./all_dirs/Ls48.beta0.42.m0.04/fort.200.total.1.csv\
 ./all_dirs/Ls48.beta0.42.m0.04/fort.200.total.2.csv\
 ./all_dirs/Ls48.beta0.42.m0.05/fort.200.total.1.csv\
 ./all_dirs/Ls48.beta0.42.m0.05/fort.200.total.2.csv\
 ./all_dirs/Ls48.beta0.44.m0.01/fort.200.total.1.csv\
 ./all_dirs/Ls48.beta0.44.m0.01/fort.200.total.2.csv\
 ./all_dirs/Ls48.beta0.44.m0.02/fort.200.total.1.csv\
 ./all_dirs/Ls48.beta0.44.m0.02/fort.200.total.2.csv\
 ./all_dirs/Ls48.beta0.44.m0.03/fort.200.total.1.csv\
 ./all_dirs/Ls48.beta0.44.m0.03/fort.200.total.2.csv\
 ./all_dirs/Ls48.beta0.44.m0.04/fort.200.total.1.csv\
 ./all_dirs/Ls48.beta0.44.m0.04/fort.200.total.2.csv\
 ./all_dirs/Ls48.beta0.44.m0.05/fort.200.total.1.csv\
 ./all_dirs/Ls48.beta0.44.m0.05/fort.200.total.2.csv\
 ./all_dirs/Ls48.beta0.46.m0.01/fort.200.total.1.csv\
 ./all_dirs/Ls48.beta0.46.m0.01/fort.200.total.2.csv\
 ./all_dirs/Ls48.beta0.46.m0.02/fort.200.total.1.csv\
 ./all_dirs/Ls48.beta0.46.m0.02/fort.200.total.2.csv\
 ./all_dirs/Ls48.beta0.46.m0.03/fort.200.total.1.csv\
 ./all_dirs/Ls48.beta0.46.m0.03/fort.200.total.2.csv\
 ./all_dirs/Ls48.beta0.46.m0.04/fort.200.total.1.csv\
 ./all_dirs/Ls48.beta0.46.m0.04/fort.200.total.2.csv\
 ./all_dirs/Ls48.beta0.46.m0.05/fort.200.total.1.csv\
 ./all_dirs/Ls48.beta0.46.m0.05/fort.200.total.2.csv\
 ./all_dirs/Ls48.beta0.55.m0.01/fort.200.total.1.csv\
 ./all_dirs/Ls48.beta0.55.m0.01/fort.200.total.2.csv\
 ./all_dirs/Ls48.beta0.55.m0.02/fort.200.total.1.csv\
 ./all_dirs/Ls48.beta0.55.m0.02/fort.200.total.2.csv\
 ./all_dirs/Ls48.beta0.55.m0.03/fort.200.total.1.csv\
 ./all_dirs/Ls48.beta0.55.m0.03/fort.200.total.2.csv\
 ./all_dirs/Ls48.beta0.55.m0.04/fort.200.total.1.csv\
 ./all_dirs/Ls48.beta0.55.m0.04/fort.200.total.2.csv\
 ./all_dirs/Ls48.beta0.55.m0.05/fort.200.total.1.csv\
 ./all_dirs/Ls48.beta0.55.m0.05/fort.200.total.2.csv\
 ./all_dirs16/Ls32.beta0.30.m0.01/fort.200.total.1.csv\
 ./all_dirs16/Ls32.beta0.30.m0.02/fort.200.total.1.csv\
 ./all_dirs16/Ls32.beta0.30.m0.03/fort.200.total.1.csv\
 ./all_dirs16/Ls32.beta0.30.m0.04/fort.200.total.1.csv\
 ./all_dirs16/Ls32.beta0.30.m0.05/fort.200.total.1.csv\
 ./all_dirs16/Ls32.beta0.32.m0.01/fort.200.total.1.csv\
 ./all_dirs16/Ls32.beta0.32.m0.02/fort.200.total.1.csv\
 ./all_dirs16/Ls32.beta0.32.m0.03/fort.200.total.1.csv\
 ./all_dirs16/Ls32.beta0.32.m0.04/fort.200.total.1.csv\
 ./all_dirs16/Ls32.beta0.32.m0.05/fort.200.total.1.csv\
 ./all_dirs16/Ls32.beta0.34.m0.01/fort.200.total.1.csv\
 ./all_dirs16/Ls32.beta0.34.m0.02/fort.200.total.1.csv\
 ./all_dirs16/Ls32.beta0.34.m0.03/fort.200.total.1.csv\
 ./all_dirs16/Ls32.beta0.34.m0.04/fort.200.total.1.csv\
 ./all_dirs16/Ls32.beta0.34.m0.05/fort.200.total.1.csv\
 ./all_dirs16/Ls32.beta0.36.m0.01/fort.200.total.1.csv\
 ./all_dirs16/Ls32.beta0.36.m0.02/fort.200.total.1.csv\
 ./all_dirs16/Ls32.beta0.36.m0.03/fort.200.total.1.csv\
 ./all_dirs16/Ls32.beta0.36.m0.04/fort.200.total.1.csv\
 ./all_dirs16/Ls32.beta0.36.m0.05/fort.200.total.1.csv\
 ./all_dirs16/Ls32.beta0.38.m0.01/fort.200.total.1.csv\
 ./all_dirs16/Ls32.beta0.38.m0.02/fort.200.total.1.csv\
 ./all_dirs16/Ls32.beta0.38.m0.03/fort.200.total.1.csv\
 ./all_dirs16/Ls32.beta0.38.m0.04/fort.200.total.1.csv\
 ./all_dirs16/Ls32.beta0.38.m0.05/fort.200.total.1.csv\
 ./all_dirs16/Ls40.beta0.30.m0.01/fort.200.total.1.csv\
 ./all_dirs16/Ls40.beta0.30.m0.02/fort.200.total.1.csv\
 ./all_dirs16/Ls40.beta0.30.m0.03/fort.200.total.1.csv\
 ./all_dirs16/Ls40.beta0.30.m0.04/fort.200.total.1.csv\
 ./all_dirs16/Ls40.beta0.30.m0.05/fort.200.total.1.csv\
 ./all_dirs16/Ls40.beta0.32.m0.01/fort.200.total.1.csv\
 ./all_dirs16/Ls40.beta0.32.m0.02/fort.200.total.1.csv\
 ./all_dirs16/Ls40.beta0.32.m0.03/fort.200.total.1.csv\
 ./all_dirs16/Ls40.beta0.32.m0.04/fort.200.total.1.csv\
 ./all_dirs16/Ls40.beta0.32.m0.05/fort.200.total.1.csv\
 ./all_dirs16/Ls40.beta0.34.m0.01/fort.200.total.1.csv\
 ./all_dirs16/Ls40.beta0.34.m0.02/fort.200.total.1.csv\
 ./all_dirs16/Ls40.beta0.34.m0.03/fort.200.total.1.csv\
 ./all_dirs16/Ls40.beta0.34.m0.04/fort.200.total.1.csv\
 ./all_dirs16/Ls40.beta0.34.m0.05/fort.200.total.1.csv\
 ./all_dirs16/Ls40.beta0.36.m0.01/fort.200.total.1.csv\
 ./all_dirs16/Ls40.beta0.36.m0.02/fort.200.total.1.csv\
 ./all_dirs16/Ls40.beta0.36.m0.03/fort.200.total.1.csv\
 ./all_dirs16/Ls40.beta0.36.m0.04/fort.200.total.1.csv\
 ./all_dirs16/Ls40.beta0.36.m0.05/fort.200.total.1.csv\
 ./all_dirs16/Ls40.beta0.38.m0.01/fort.200.total.1.csv\
 ./all_dirs16/Ls40.beta0.38.m0.02/fort.200.total.1.csv\
 ./all_dirs16/Ls40.beta0.38.m0.03/fort.200.total.1.csv\
 ./all_dirs16/Ls40.beta0.38.m0.04/fort.200.total.1.csv\
 ./all_dirs16/Ls40.beta0.38.m0.05/fort.200.total.1.csv\
 ./all_dirs16/Ls48.beta0.30.m0.01/fort.200.total.1.csv\
 ./all_dirs16/Ls48.beta0.30.m0.02/fort.200.total.1.csv\
 ./all_dirs16/Ls48.beta0.30.m0.03/fort.200.total.1.csv\
 ./all_dirs16/Ls48.beta0.30.m0.04/fort.200.total.1.csv\
 ./all_dirs16/Ls48.beta0.30.m0.05/fort.200.total.1.csv\
 ./all_dirs16/Ls48.beta0.32.m0.01/fort.200.total.1.csv\
 ./all_dirs16/Ls48.beta0.32.m0.02/fort.200.total.1.csv\
 ./all_dirs16/Ls48.beta0.32.m0.03/fort.200.total.1.csv\
 ./all_dirs16/Ls48.beta0.32.m0.04/fort.200.total.1.csv\
 ./all_dirs16/Ls48.beta0.32.m0.05/fort.200.total.1.csv\
 ./all_dirs16/Ls48.beta0.34.m0.01/fort.200.total.1.csv\
 ./all_dirs16/Ls48.beta0.34.m0.02/fort.200.total.1.csv\
 ./all_dirs16/Ls48.beta0.34.m0.03/fort.200.total.1.csv\
 ./all_dirs16/Ls48.beta0.34.m0.04/fort.200.total.1.csv\
 ./all_dirs16/Ls48.beta0.34.m0.05/fort.200.total.1.csv\
 ./all_dirs16/Ls48.beta0.36.m0.01/fort.200.total.1.csv\
 ./all_dirs16/Ls48.beta0.36.m0.02/fort.200.total.1.csv\
 ./all_dirs16/Ls48.beta0.36.m0.03/fort.200.total.1.csv\
 ./all_dirs16/Ls48.beta0.36.m0.04/fort.200.total.1.csv\
 ./all_dirs16/Ls48.beta0.36.m0.05/fort.200.total.1.csv\
 ./all_dirs16/Ls48.beta0.38.m0.01/fort.200.total.1.csv\
 ./all_dirs16/Ls48.beta0.38.m0.02/fort.200.total.1.csv\
 ./all_dirs16/Ls48.beta0.38.m0.03/fort.200.total.1.csv\
 ./all_dirs16/Ls48.beta0.38.m0.04/fort.200.total.1.csv\
 ./all_dirs16/Ls48.beta0.38.m0.05/fort.200.total.1.csv ./fort.200.analysis.set
	. ../Scripts/lib.sh&&cd .&&../ProtocolUtils/log ../Scripts/pbp_data_processing.py fort.200.analysis.set

