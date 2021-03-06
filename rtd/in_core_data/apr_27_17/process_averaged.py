import matplotlib.pyplot as plt
import numpy as np
import csv
import matplotlib.patches as mpatches

def main():
    '''
    Description of the data files are followed:
    The files with "nopump" are the pump-off measurement, and the others are the pump-on measurement.
    The "139" are the first T7 PRO device, and the "166" are the second one.
    Each file has 15 columns. The first column is the time in second.
    The remaining columns are the RTD readout temperatures in C.
    Since the LogM software will start a new log file if the first log file exceeds a certain size, the "*_1"
    file follows the "*_0" file, i.e., the time are continuous in these two files.
    The port assignments are (the numbering starts at 0):

    The 139 device:
    port          RTD

    0 to 6        RTD 0 to 6 in probe A
    7 is not used (broken)
    8             RTD 8 in probe A
    9 to 13       RTD 0 to 4 in probe B

    The 166 device:
    port          RTD

    0 to 3        RTD 5 to 8 in probe B
    4 to 12       RTD 0 to 8 in probe C
    13            RTD 7 in probe A

    returns plots

    '''

########################################################################################################################
# Load Raw data
    # 139_pab
########################################################################################################################
    pab_0 = read_data('139_pab_0.dat')
    pab_1 = read_data('139_pab_1.dat')

    pab_off =  pab_0[0][-1]

    pab_time = pab_0[0]
    for item in pab_1[0]:
        pab_time.append(item + pab_off )

    pab_dat = []

    for ind, im in enumerate(pab_0[1]):

        li = []
        for itm in im:
            li.append(itm)
        for itm in pab_1[1][ind]:
            li.append(itm)

        pab_dat.append(li)
################################################################
# 166_pbc load
################################################################

    pbc_0 = read_data('166_pbc_0.dat')
    pbc_1 = read_data('166_pbc_1.dat')

    pbc_off =  pbc_0[0][-1]


    pbc_time = pbc_0[0]
    for item in pbc_1[0]:
        pbc_time.append(item + pbc_off )

    pbc_dat = []

    for ind, im in enumerate(pbc_0[1]):

        li = []
        for itm in im:
            li.append(itm)
        for itm in pbc_1[1][ind]:
            li.append(itm)

        pbc_dat.append(li)

################################################################
# 166_pbc nopump load
################################################################

    pbcnp_0 = read_data('166_pbc_nopump_100kw_0.dat')
    pbcnp_1 = read_data('166_pbc_nopump_100kw_1.dat')

    pbcnp_off =  pbcnp_0[0][-1]

    pbcnp_time = pbcnp_0[0]

    for item in pbcnp_1[0]:
        pbcnp_time.append(item + pbcnp_off )

    pbcnp_dat = []

    for ind, im in enumerate(pbcnp_0[1]):

        li = []
        for itm in im:
            li.append(itm)
        for itm in pbcnp_1[1][ind]:
            li.append(itm)

        pbcnp_dat.append(li)


################################################################
# 139_pbc nopump load
################################################################

    pabnp_0 = read_data('139_pab_nopump_100kw_0.dat')
    pabnp_1 = read_data('139_pab_nopump_100kw_1.dat')

    pabnp_off =  pabnp_0[0][-1]

    pabnp_time = pabnp_0[0]
    for item in pabnp_1[0]:
        pabnp_time.append(item + pabnp_off )

    pabnp_dat = []

    for ind, im in enumerate(pabnp_0[1]):

        li = []
        for itm in im:
            li.append(itm)
        for itm in pabnp_1[1][ind]:
            li.append(itm)

        pabnp_dat.append(li)

#######################################################################################################################
# Seperate data by probe qtih pumps
#######################################################################################################################

    pa_dat = pab_dat[:7]
    pa_dat.append(pbc_dat[13])
    pa_dat.append(pab_dat[8])

    pb_dat = pab_dat[9:]
    for item in pbc_dat[:4]:
        pb_dat.append(item)


    pc_dat = pbc_dat[4:13]

#######################################################################################################################
#Generate Times for each probe
#######################################################################################################################
    pa_time = []
    for item in pa_dat:
        pa_time.append([ind * 0.5 for  ind, it in enumerate(item)])
    pb_time = [ind * 0.5 for  ind, it in enumerate(pb_dat[0])]
    pc_time = [ind * 0.5 for  ind, it in enumerate(pc_dat[0])]


#######################################################################################################################
# Seperate data by probe  NO pumps
#######################################################################################################################
    pnpa_dat = pabnp_dat[:7]
    pnpa_dat.append(pbcnp_dat[13])
    pnpa_dat.append(pabnp_dat[8])


    pnpb_dat = pabnp_dat[9:]

    for item in pbcnp_dat[:4]:
        pnpb_dat.append(item)


    pnpc_dat = pbcnp_dat[4:13]

#######################################################################################################################
#Generate Times for each probe
#######################################################################################################################

  #  pnpa_time = [ind * 0.5 for  ind, it in enumerate(pnpa_dat[0])]
  #  pnpb_time = [ind * 0.5 for  ind, it in enumerate(pnpb_dat[0])]
  #  pnpc_time = [ind * 0.5 for  ind, it in enumerate(pnpc_dat[0])]



########################################################################################################################
    # Generate test plots
########################################################################################################################

    #for ind, it in enumerate(pa_dat):
    #    plt.plot(pa_time[ind], it)


########################################################################################################################
    # Create Axially Averaged Data and Times (2Hz sampling rate)
########################################################################################################################
     ####################### pa_sum
    pa_sum = []

    for ind, it in enumerate(pa_dat[0]):
        try:
            pa_sum.append(sum([float(item) for item in [it, pa_dat[1][ind], pa_dat[2][ind], pa_dat[3][ind],
                                                        pa_dat[4][ind], pa_dat[5][ind], pa_dat[6][ind],
                                                        pa_dat[7][ind], pa_dat[8][ind]]])/9)
        except IndexError:
            pass

    ########################### pb_sum
    pb_sum = []

    for ind, it in enumerate(pb_dat[0]):
        try:
            pb_sum.append(sum([float(item) for item in [it, pb_dat[1][ind], pb_dat[2][ind], pb_dat[3][ind], pb_dat[4][ind], pb_dat[5][ind], pb_dat[6][ind], pb_dat[7][ind], pb_dat[8][ind]]])/9)
        except IndexError:
            pass

    ###########################  pc_sum
    pc_sum = []

    for ind, it in enumerate(pc_dat[0]):
        try:
            pc_sum.append(sum([float(item) for item in [it, pc_dat[1][ind], pc_dat[2][ind], pc_dat[3][ind], pc_dat[4][ind], pc_dat[5][ind], pc_dat[6][ind], pc_dat[7][ind], pc_dat[8][ind]]])/9)
        except IndexError:
            pass

    ####################### pnpa_sum
    pnpa_sum = []

    for ind, it in enumerate(pnpa_dat[0]):
        try:
            pnpa_sum.append(sum([float(item) for item in [it, pnpa_dat[1][ind], pnpa_dat[2][ind], pnpa_dat[3][ind], pnpa_dat[4][ind], pnpa_dat[5][ind], pnpa_dat[6][ind], pnpa_dat[7][ind], pnpa_dat[8][ind]]])/9)
        except IndexError:
            pass

    ######################## pnpb_sum
    pnpb_sum = []

    for ind, it in enumerate(pnpb_dat[0]):
        try:
            pnpb_sum.append(sum([float(item) for item in [it, pnpb_dat[1][ind], pnpb_dat[2][ind], pnpb_dat[3][ind], pnpb_dat[4][ind], pnpb_dat[5][ind], pnpb_dat[6][ind], pnpb_dat[7][ind], pnpb_dat[8][ind]]])/9)
        except IndexError:
            pass

    ######################## pnpc_sum
    pnpc_sum = []

    for ind, it in enumerate(pnpc_dat[0]):
        try:
            pnpc_sum.append(sum([float(item) for item in [it, pnpc_dat[1][ind], pnpc_dat[2][ind], pnpc_dat[3][ind], pnpc_dat[4][ind], pnpc_dat[5][ind], pnpc_dat[6][ind], pnpc_dat[7][ind], pnpc_dat[8][ind]]])/9)
        except IndexError:
            pass

######################### Sum Times
    pa_sum_time = [ind * 0.5/60 for ind, item in enumerate(pa_sum)]
    pb_sum_time = [ind * 0.5/60 for ind, item in enumerate(pb_sum)]
    pc_sum_time = [ind * 0.5/60 for ind, item in enumerate(pc_sum)]

    pnpa_sum_time = [ind * 0.5/60 for ind, item in enumerate(pnpa_sum)]
    pnpb_sum_time = [ind * 0.5/60 for ind, item in enumerate(pnpb_sum)]
    pnpc_sum_time = [ind * 0.5/60 for ind, item in enumerate(pnpc_sum)]


########################################################################################################################
#  GENERATE PLOTS Of AXIALLY AVERAGED DATA
########################################################################################################################
    plt.plot(pa_sum_time, pa_sum, 'b', label='Probe A')
    plt.plot(pb_sum_time, pb_sum, 'g', label='Probe B')
    plt.plot(pc_sum_time, pc_sum, 'r', label='Probe C')
    plt.xlabel('Time (Minutes)')
    plt.ylabel('Temperature (Celsius)')
    plt.title('Transient Temperature Data for 3 Probe Multipower Test')

    plt.legend(loc=2)
    plt.savefig('axially_averaged.png')
    plt.clf()

    plt.plot(pnpa_sum_time, pnpa_sum, 'b', label='Probe A')
    plt.plot(pnpb_sum_time, pnpb_sum, 'g', label='Probe B')
    plt.plot(pnpc_sum_time, pnpc_sum, 'r', label='Probe C')
    plt.xlabel('Time (Minutes)')
    plt.ylabel('Temperature (Celsius)')
    plt.title('Temperature Data for 3 Probe Multipower Test No Pumps')

    plt.legend(loc=2)
    plt.savefig('axially_averaged_nopumps.png')
    plt.clf()


#######################################################################################################################
# GENERATE PLOTS OF AXIALLY DEPENDANT TEMPERATURES
#######################################################################################################################

    si50 = int(6.2 * 60 * 2)
    ei50 = int(18.6 * 60 * 2)

    si100 = int(22 * 60 * 2)
    ei100 = int(33 * 60 * 2)

    si250 = int(36 * 60 * 2)
    ei250 = int(48.5 * 60 * 2)

    si500 = int(52 * 60 * 2)
    ei500 = int(64 * 60 * 2)

    print si50, ei50
    print si100, ei100
    print si250, ei250
    print si500, ei500

    rtd_locs = [14.51 + (4.7625* it) for it in range(9)]
    print rtd_locs


    a50 = []
    a100 = []
    a250 = []
    a500 = []

    b50 = []
    b100 = []
    b250 = []
    b500 = []

    c50 = []
    c100 = []
    c250 = []
    c500 = []

    for ind, it in enumerate(pa_dat):
        pa_dat[ind] = [float(num) for num in pa_dat[ind]]
        pb_dat[ind] = [float(num) for num in pb_dat[ind]]
        pc_dat[ind] = [float(num) for num in pc_dat[ind]]

    for index, it in enumerate(rtd_locs):

        a50.append(sum(pa_dat[index][si50:ei50])/len(pa_dat[index][si50:ei50]))
        a100.append(sum(pa_dat[index][si100:ei100])/len(pa_dat[index][si100:ei100]))
        a250.append(sum(pa_dat[index][si250:ei250])/len(pa_dat[index][si250:ei250]))
        a500.append(sum(pa_dat[index][si500:ei500])/len(pa_dat[index][si500:ei500]))

        b50.append(sum(pb_dat[index][si50:ei50])/len(pb_dat[index][si50:ei50]))
        b100.append(sum(pb_dat[index][si100:ei100])/len(pb_dat[index][si100:ei100]))
        b250.append(sum(pb_dat[index][si250:ei250])/len(pb_dat[index][si250:ei250]))
        b500.append(sum(pb_dat[index][si500:ei500])/len(pb_dat[index][si500:ei500]))

        c50.append(sum(pc_dat[index][si50:ei50])/len(pc_dat[index][si50:ei50]))
        c100.append(sum(pc_dat[index][si100:ei100])/len(pc_dat[index][si100:ei100]))
        c250.append(sum(pc_dat[index][si250:ei250])/len(pc_dat[index][si250:ei250]))
        c500.append(sum(pc_dat[index][si500:ei500])/len(pc_dat[index][si500:ei500]))



    ali = [a50, a100, a250, a500]
    bli = [b50, b100, b250, b500]
    cli = [c50, c100, c250, c500]



    a50err = []
    a100err = []
    a250err = []
    a500err = []

    b50err = []
    b100err = []
    b250err = []
    b500err = []


    c50err = []
    c100err = []
    c250err = []
    c500err = []

    for index, itm in enumerate(a50):



        a50err.append(max(pa_dat[index][si50:ei50])-a50[index])
        a100err.append(max(pa_dat[index][si100:ei100])-a100[index])
        a250err.append(max(pa_dat[index][si250:ei250])-a250[index])
        a500err.append(max(pa_dat[index][si500:ei500])-a500[index])

        b50err.append(max(pb_dat[index][si50:ei50])-b50[index])
        b100err.append(max(pb_dat[index][si100:ei100])-b100[index])
        b250err.append(max(pb_dat[index][si250:ei250])-b250[index])
        b500err.append(max(pb_dat[index][si500:ei500])-b500[index])

        c50err.append(max(pc_dat[index][si50:ei50])-c50[index])
        c100err.append(max(pc_dat[index][si100:ei100])-c100[index])
        c250err.append(max(pc_dat[index][si250:ei250])-c250[index])
        c500err.append(max(pc_dat[index][si500:ei500])-c500[index])


    aerr= [a50err, a100err, a250err, a500err]
    berr= [b50err, b100err, b250err, b500err]
    cerr= [c50err, c100err, c250err, c500err]

###########################################
    #Probe A
###########################################

    for ind, item in enumerate(ali):
        powers = [50, 100, 250, 500]
        clr = ['b', 'g', 'y', 'r']

        plt.errorbar(rtd_locs, item, yerr = aerr[ind],  fmt ='{}o-'.format(clr[ind]), label='{} kW'.format(powers[ind]))

    plt.xlabel('Distance from tip of probe (cm)')
    plt.ylabel('Temperature (C)')
    plt.title('Temperature versus Axial Location in Probe A')
    plt.legend(loc=2)
    plt.savefig('pa_loc_v_temp.png')
    plt.show()
    plt.clf()

###########################################
    #Probe B
###########################################

    for ind, item in enumerate(bli):
        powers = [50, 100, 250, 500]
        clr = ['b', 'g', 'y', 'r']

        plt.errorbar(rtd_locs, item, yerr = berr[ind],  fmt = '{}o-'.format(clr[ind]), label='{} kW'.format(powers[ind]))

    plt.xlabel('Distance from tip of probe (cm)')
    plt.ylabel('Temperature (C)')
    plt.title('Temperature versus Axial Location in Probe B')
    plt.legend(loc=2)
    plt.savefig('pb_loc_v_temp.png')
    plt.show()
    plt.clf()

###########################################
    #Probe C
###########################################

    for ind, item in enumerate(cli):
        powers = [50, 100, 250, 500]
        clr = ['b', 'g', 'y', 'r']

        plt.errorbar(rtd_locs, item,yerr=cerr[ind], fmt= '{}o-'.format(clr[ind]), label='{} kW'.format(powers[ind]))

    plt.xlabel('Distance from tip of probe (cm)')
    plt.ylabel('Temperature (C)')
    plt.title('Temperature versus Axial Location in Probe C')
    plt.legend(loc=2)
    plt.savefig('pc_loc_v_temp.png')
    plt.show()
    plt.clf()


#######################################################################################################################
# GENERATE PLOTS OF AXIALLY DEPENDANT TEMPERATURES FOR NOPUMPS
#######################################################################################################################

    si1001 = int(5 * 60 * 2)
    ei1001 = int(29 * 60 * 2)

    si250 = int(33 * 60 * 2)
    ei250 = int(60 * 60 * 2)

    si1002 = int(63 * 60 * 2)
    ei1002 = int(89 * 60 * 2)


    rtd_locs = [14.51 + (4.7625* it) for it in range(9)]



    a1001 = []
    a250 = []
    a1002 = []

    b1001 = []
    b250 = []
    b1002 = []

    c1001 = []
    c250 = []
    c1002 = []

    for ind, it in enumerate(pa_dat):
        pnpa_dat[ind] = [float(num) for num in pnpa_dat[ind]]
        pnpb_dat[ind] = [float(num) for num in pnpb_dat[ind]]
        pnpc_dat[ind] = [float(num) for num in pnpc_dat[ind]]

    for index, it in enumerate(rtd_locs):

        a1001.append(sum(pnpa_dat[index][si1001:ei1001])/len(pnpa_dat[index][si1001:ei1001]))
        a250.append(sum(pnpa_dat[index][si250:ei250])/len(pnpa_dat[index][si250:ei250]))
        a1002.append(sum(pnpa_dat[index][si1002:ei1002])/len(pnpa_dat[index][si1002:ei1002]))

        b1001.append(sum(pnpb_dat[index][si1001:ei1001])/len(pnpb_dat[index][si1001:ei1001]))
        b250.append(sum(pnpb_dat[index][si250:ei250])/len(pnpb_dat[index][si250:ei250]))
        b1002.append(sum(pnpb_dat[index][si1002:ei1002])/len(pnpb_dat[index][si1002:ei1002]))

        c1001.append(sum(pnpc_dat[index][si1001:ei1001])/len(pnpc_dat[index][si1001:ei1001]))
        c250.append(sum(pnpc_dat[index][si250:ei250])/len(pnpc_dat[index][si250:ei250]))
        c1002.append(sum(pnpc_dat[index][si1002:ei1002])/len(pnpc_dat[index][si1002:ei1002]))


    ali2 = [a1001, a250, a1002]
    bli2 = [b1001, b250, b1002]
    cli2 = [c1001, c250, c1002]

    a1001err = []
    a250err = []
    a1002err = []

    b1001err = []
    b250err = []
    b1002err = []

    c1001err = []
    c250err = []
    c1002err = []


    for index, itm in enumerate(a1001):


        a1001err.append(max(pnpa_dat[index][si1001:ei1001])-a1001[index])
        a250err.append(max(pnpa_dat[index][si250:ei250])-a250[index])
        a1002err.append(max(pnpa_dat[index][si1002:ei1002])-a1001[index])

        b1001err.append(max(pnpb_dat[index][si1001:ei1001])-b1001[index])
        b250err.append(max(pnpb_dat[index][si250:ei250])-b250[index])
        b1002err.append(max(pnpb_dat[index][si1002:ei1002])-b1002[index])

        c1001err.append(max(pnpc_dat[index][si1001:ei1001])-c1001[index])
        c250err.append(max(pnpc_dat[index][si250:ei250])-c250[index])
        c1002err.append(max(pnpc_dat[index][si1002:ei1002])-c1002[index])


    anperr = [a1001err, a250err, a1002err]
    bnperr = [b1001err, b250err, b1002err]
    cnperr = [c1001err, c250err, c1002err]


###########################################
    #Probe A NP
###########################################

    for ind, item in enumerate(ali2):
        powers = [ 100, 250, 100]
        clr = ['b', 'g', 'y', 'r']

        plt.errorbar(rtd_locs, item,yerr= anperr[ind], fmt = '{}o-'.format(clr[ind]), label='{} kW'.format(powers[ind]))

    plt.xlabel('Distance from tip of probe (cm)')
    plt.ylabel('Temperature (C)')
    plt.title('Temperature versus Axial Location in Probe A No Pumps')
    plt.legend(loc=2)
    plt.savefig('pnpa_loc_v_temp.png')
    plt.show()
    plt.clf()

###########################################
    #Probe B NP
###########################################

    for ind, item in enumerate(bli2):
        powers = [ 100, 250, 100]
        clr = ['b', 'g', 'y', 'r']

        plt.errorbar(rtd_locs, item,yerr=bnperr[ind], fmt='{}o-'.format(clr[ind]), label='{} kW'.format(powers[ind]))

    plt.xlabel('Distance from tip of probe (cm)')
    plt.ylabel('Temperature (C)')
    plt.title('Temperature versus Axial Location in Probe B No Pumps')
    plt.legend(loc=2)
    plt.savefig('pnpb_loc_v_temp.png')
    plt.show()
    plt.clf()

###########################################
    #Probe C NP
###########################################

    for ind, item in enumerate(cli2):
        powers = [ 100 , 250, 100]
        clr = ['b', 'g', 'y', 'r']

        plt.errorbar(rtd_locs, item,yerr = cnperr[ind], fmt = '{}o-'.format(clr[ind]), label='{} kW'.format(powers[ind]))

    plt.xlabel('Distance from tip of probe (cm)')
    plt.ylabel('Temperature (C)')
    plt.title('Temperature versus Axial Location in Probe C No Pumps')
    plt.legend(loc=2)
    plt.savefig('pnpc_loc_v_temp.png')
    plt.show()
    plt.clf()

    ##########################################################

    plt.plot(rtd_locs, ali[2], 'bo-', label='Probe A' )
    plt.plot(rtd_locs, bli[2], 'ro-', label='Probe B' )
    plt.plot(rtd_locs, cli[2], 'go-', label='Probe C' )
    plt.xlabel('Distance from tip of probe (cm)')
    plt.ylabel('Temperature (C)')
    plt.title('Temperature versus Axial Location for 250 kW Pumps')
    plt.savefig('tvloc_250p.png')
    plt.legend(loc=1)
    plt.show()
    plt.clf()

    plt.plot(rtd_locs, ali2[1], 'bo-', label='Probe A' )
    plt.plot(rtd_locs, bli2[1], 'ro-', label='Probe B' )
    plt.plot(rtd_locs, cli2[1], 'go-', label='Probe C' )
    plt.xlabel('Distance from tip of probe (cm)')
    plt.ylabel('Temperature (C)')
    plt.title('Temperature versus Axial Location for 250 kW No Pumps')
    plt.savefig('tvloc_250np.png')
    plt.legend(loc=2)
    plt.show()
    plt.clf()


    plt.plot(rtd_locs, ali[1], 'bo-', label='Probe A' )
    plt.plot(rtd_locs, bli[1], 'ro-', label='Probe B' )
    plt.plot(rtd_locs, cli[1], 'go-', label='Probe C' )
    plt.xlabel('Distance from tip of probe (cm)')
    plt.ylabel('Temperature (C)')
    plt.title('Temperature versus Axial Location for 100 kW Pumps')
    plt.savefig('tvloc_100p.png')
    plt.legend(loc=1)
    plt.show()
    plt.clf()


    plt.plot(rtd_locs, ali2[0], 'bo-', label='Probe A' )
    plt.plot(rtd_locs, bli2[0], 'ro-', label='Probe B' )
    plt.plot(rtd_locs, cli2[0], 'go-', label='Probe C' )

    plt.xlabel('Distance from tip of probe (cm)')
    plt.ylabel('Temperature (C)')
    plt.title('Temperature versus Axial Location for 100 kW No Pumps')
    plt.savefig('tvloc_100np.png')
    plt.legend(loc=2)
    plt.show()
    plt.clf()




def read_data(fname):
    '''
    :param fname: filename of loaded file
    :return: Tuple
    1st item is tru_time (adjusted time to start at 0 seconds and step in 0.5 secs)
    2nd item is the data as a list of lists. each list contains a column from the input

    time can be used instead of tru_time to return the time provided by the output file
    '''


    time = []
    data = []
    d = []

    with open(fname, 'rb') as infile:
        spamreader = csv.reader(infile, delimiter='	')
        for row in spamreader:
            time.append(row[0])
            data.append(row[1:])

    ref = data[0]

    for index, item in enumerate(ref):
        d.append([it[index] for it in data])



    tru_time = [index * 0.5 for index, i in enumerate(time)]

    return (tru_time, d)

if __name__ == '__main__':
    main()