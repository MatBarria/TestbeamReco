import ROOT
import os

## Define global variables
marg=0.05
font=43 # Helvetica
# tsize=32
tsize=38 #35

### Paths and directories' functions
def getOutputDir(dataset):
    outdir = "../output/%s/" % dataset
    return outdir

def CreateFolder(outdir, title, overwrite = False):
    outdir2 = os.path.join(outdir,title)

    if overwrite:
        os.mkdir(outdir2)
    else:
        if not os.path.exists(outdir2):
                os.mkdir(outdir2)
        else:
            i = 1
            while(os.path.exists(outdir2)):
                    outdir2 = outdir2[0:-2] + str(i) + outdir2[-1]
                    i+=1
            os.mkdir(outdir2)
    print(outdir2,"created.")
    return outdir2

def GetPlotsDir(outdir, macro_title):
    outdir_tmp = os.path.join(outdir, macro_title)
    if not (os.path.exists(outdir_tmp)):
        outdir_tmp = CreateFolder(outdir, macro_title, True)

    return outdir_tmp


### Style functions
def ForceStyle():
    ## Defining Style
    ROOT.gStyle.SetPadTopMargin(marg)       #0.05
    ROOT.gStyle.SetPadRightMargin(marg)     #0.05
    ROOT.gStyle.SetPadBottomMargin(2*marg)  #0.10
    ROOT.gStyle.SetPadLeftMargin(2*marg)    #0.10

    ROOT.gStyle.SetPadTickX(1)
    ROOT.gStyle.SetPadTickY(1)

    ROOT.gStyle.SetTextFont(font)
    ROOT.gStyle.SetLabelFont(font,"x")
    ROOT.gStyle.SetTitleFont(font,"x")
    ROOT.gStyle.SetLabelFont(font,"y")
    ROOT.gStyle.SetTitleFont(font,"y")
    ROOT.gStyle.SetLabelFont(font,"z")
    ROOT.gStyle.SetTitleFont(font,"z")

    ROOT.gStyle.SetTextSize(tsize)
    ROOT.gStyle.SetLabelSize(tsize-4,"x")
    ROOT.gStyle.SetTitleSize(tsize,"x")
    ROOT.gStyle.SetLabelSize(tsize-4,"y")
    ROOT.gStyle.SetTitleSize(tsize,"y")
    ROOT.gStyle.SetLabelSize(tsize-4,"z")
    ROOT.gStyle.SetTitleSize(tsize,"z")

    ROOT.gStyle.SetLegendFont(font)
    ROOT.gStyle.SetLegendTextSize(tsize)
    ROOT.gStyle.SetLegendBorderSize(0)
    ROOT.gStyle.SetLegendFillColor(0)

    ROOT.gStyle.SetTitleXOffset(1.0)
    ROOT.gStyle.SetTitleYOffset(1.0)
    ROOT.gStyle.SetOptTitle(0)
    # ROOT.gStyle.SetOptStat(0)

    ROOT.gStyle.SetHistLineWidth(4)

    ROOT.gStyle.SetGridColor(921)
    ROOT.gStyle.SetGridStyle()

    ROOT.gROOT.ForceStyle()


def BeamInfo():
    text = ROOT.TLatex()
    text.SetTextSize(tsize-4)
    text.DrawLatexNDC(2*marg+0.005,1-marg+0.01,"#bf{FNAL 120 GeV proton beam}")

def SensorInfo(sensor="Name", bias_voltage="", write_bv=True,adjustleft=0):
    text = ROOT.TLatex()
    text.SetTextSize(tsize-4)
    text.SetTextAlign(31)
    if bias_voltage:
        text.DrawLatexNDC(1-marg-0.005-adjustleft,1-marg+0.01,"#bf{"+str(sensor) + ", "+str(bias_voltage)+"}")
    else:
        text.DrawLatexNDC(1-marg-0.005-adjustleft,1-marg+0.01,"#bf{"+str(sensor)+"}")

def SensorInfoSmart(dataset, adjust=0.00):
    name ="Not defined"
    bias_voltage = "X"

    if GetGeometry(dataset):
        name = GetGeometry(dataset)['sensor']
        bias_voltage = GetBV(dataset)

    SensorInfo(name,bias_voltage,True,adjust)


### Return-value functions
def GetMargin():
    return marg

def GetFont():
    return font

def GetSize():
    return tsize

def GetPadCenter():
    return (1 + marg)/2


### Colors
def GetColors(color_blind = False):
    strip_colors = [416+2, 432+2, 600, 880, 632, 400+2, 600-5]
    ## [#kGreen+2, #kCyan+2, #kBlue, #kViolet, #kRed, #kYellow+2, #kBlue-3]
    if color_blind:
        color_RGB = [[51,34,136],[51,187,238],[17,119,51],[153,153,51],[204,102,119],[136,34,85],[128,128,128]]
        # [indigo, cyan, green, olive, rose, wine]
        
        for i in range(0,len(strip_colors)):
            strip_colors[i] = ROOT.TColor.GetColor(color_RGB[i][0],color_RGB[i][1],color_RGB[i][2])

    return strip_colors


### Names and strings
def GetGeometry(name):
    sensor_dict = {}

    this_name = RemoveBV(name)

    if (this_name in sensorsGeom2022):
        sensor_dict = sensorsGeom2022[this_name]
    elif (this_name in sensorsGeom2023):
        sensor_dict = sensorsGeom2023[this_name]
    else:
        print("Sensor not found in any dictionary :(")

    return sensor_dict

def RemoveBV(name):
    name_split=name.split('_')
    if name_split[-1][-1]=="V":
        name='_'.join(str(name_split[i]) for i in range(len(name_split)-1))
    return name

def GetBV(name):
    name_split=name.split('_')
    if name_split[-1][-1]=="V":
        return name_split[-1]
    else:
        return ""


### 2022 Sensors' information dictionaries
# Dataset_name: {'sensor': <name>, 'pitch': [micron], 'stripWidth': [micron], "BV": [V], "length": [mm]},
sensorsGeom2022 = { "EIC_W2_1cm_500up_300uw": {'sensor': "BNL 10-300", 'pitch': 500, 'stripWidth': 300, "BV": 240, "length": 10.0},
                    "EIC_W1_1cm_500up_200uw": {'sensor': "BNL 10-200", 'pitch': 500, 'stripWidth': 200, "BV": 255, "length": 10.0},
                    "EIC_W2_1cm_500up_100uw": {'sensor': "BNL 10-100", 'pitch': 500, 'stripWidth': 100, "BV": 220, "length": 10.0},
                    "EIC_W1_1cm_100up_50uw": {'sensor': "EIC_1cm_100up_50uw", 'pitch': 100, 'stripWidth': 50, "BV": 240, "length": 10.0},
                    "EIC_W1_1cm_200up_100uw": {'sensor': "EIC_1cm_200up_100uw", 'pitch': 200, 'stripWidth': 100, "BV": 240, "length": 10.0},
                    "EIC_W1_1cm_300up_150uw": {'sensor': "EIC_1cm_300up_150uw", 'pitch': 300, 'stripWidth': 150, "BV": 240, "length": 10.0},
                    "EIC_W1_UCSC_2p5cm_500up_200uw": {'sensor': "EIC_2p5cm_UCSC_500up_200uw", 'pitch': 500, 'stripWidth': 200, "BV": 330, "length": 25.0},
                    "EIC_W1_2p5cm_500up_200uw": {'sensor': "BNL 25-200", 'pitch': 500, 'stripWidth': 200, "BV": 215, "length": 25.0},
                    "HPK_Eb_1cm_80up_45uw": {'sensor': "HPK_Eb_80up_45uw", 'pitch': 80, 'stripWidth': 45, "BV": 170, "length": 10.0},
                    "EIC_W1_0p5cm_500up_200uw_1_7": {'sensor': "EIC_1_7_0p5cm_500up_200uw", 'pitch': 500, 'stripWidth': 200, "BV": 240, "length": 5.0},
                    "EIC_W1_0p5cm_500up_200uw_1_4": {'sensor': "BNL 5-200", 'pitch': 500, 'stripWidth': 200, "BV": 245, "length": 5.0},
                    "BNL_500um_squares_175V": {'sensor': "BNL_squares_1cm_500up_300uw", 'pitch': 500, 'stripWidth': 100, "BV": 175},
                    "BNL2021_22_medium_150up_80uw": {'sensor': "BNL2021_V2_150up_80uw", 'pitch': 150, 'stripWidth': 80, "BV": 285},
                    "IHEP_W1_I_150up_80uw": {'sensor': "IHEP_1cm_150up_80uw", 'pitch': 150, 'stripWidth': 80, "BV": 185},
}

# 'position_oneStrip': Std Dev from fit, 'position_oneStrip_E': Statistical error from fit, 'position_oneStripRMS': RMS WITH OnMetal cut,
# 'position_oneStrip_StdDev': RMS WITHOUT OnMetal cut (This is the value used in the paper)
resolutions2022 = {
    "EIC_W2_1cm_500up_300uw_240V": {'position_oneStrip'  : 75.92, 'position_oneStrip_E': 0.18, 'position_oneStripRMS': 78.11,
                                    'position_oneStrip_StdDev': 82.71,
                                    'position_twoStrip'  : 15.74, 'position_twoStrip_E': 0.08,
                                    'efficiency_oneStrip': 0.51, 'efficiency_twoStrip' : 0.49},
    "EIC_W1_1cm_500up_200uw_255V": {'position_oneStrip'  : 81.89, 'position_oneStrip_E': 0.08, 'position_oneStripRMS': 54.75,
                                    'position_oneStrip_StdDev': 81.86,
                                    'position_twoStrip'  : 18.49, 'position_twoStrip_E': 0.02,
                                    'efficiency_oneStrip': 0.43, 'efficiency_twoStrip' : 0.57},
    "EIC_W2_1cm_500up_100uw_220V": {'position_oneStrip'  : 66.03, 'position_oneStrip_E': 0.10, 'position_oneStripRMS': 27.84,
                                    'position_oneStrip_StdDev': 68.89,
                                    'position_twoStrip'  : 19.23, 'position_twoStrip_E': 0.02,
                                    'efficiency_oneStrip': 0.23, 'efficiency_twoStrip' : 0.77},
    "EIC_W1_2p5cm_500up_200uw_215V": {'position_oneStrip'  : 121.5, 'position_oneStrip_E': 0.10, 'position_oneStripRMS': 70.93,
                                      'position_oneStrip_StdDev': 128.10,
                                      'position_twoStrip'  : 31.32, 'position_twoStrip_E': 0.12,
                                      'efficiency_oneStrip': 0.82, 'efficiency_twoStrip' : 0.18},
    "EIC_W1_0p5cm_500up_200uw_1_4_245V": {'position_oneStrip'  : 59.39, 'position_oneStrip_E': 0.08, 'position_oneStripRMS': 51.79,
                                          'position_oneStrip_StdDev': 60.93,
                                          'position_twoStrip'  : 11.76, 'position_twoStrip_E': 0.02,
                                          'efficiency_oneStrip': 0.35, 'efficiency_twoStrip' : 0.65},
    "HPK_Eb_1cm_80up_45uw": {'position_oneStrip'  : 11.91, 'position_oneStrip_E': 0.00, 'position_oneStripRMS': 13.83,
                             'position_twoStrip'  :  9.36, 'position_twoStrip_E': 0.00,
                             'efficiency_oneStrip': 0.50, 'efficiency_twoStrip' : 0.50},
    "BNL2021_22_medium_150up_80uw_285V": {'position_oneStrip'  : 14.0, 'position_oneStrip_E': 0.00, 'position_oneStripRMS': 22.35,
                                          'position_twoStrip'  : 8.01, 'position_twoStrip_E': 0.00,
                                          'efficiency_oneStrip': 0.50, 'efficiency_twoStrip': 0.50},
}

resolutions2022OneStripChannel = {
    "EIC_W2_1cm_500up_300uw_240V": {'resOneStrip': [-1.00, 81.75, 83.41, 83.40, 82.10, -1.00, -1.00], ## Std Dev
                                  # 'resOneStrip': [-1.00, 75.61, 75.73, 77.48, 77.80, -1.00, -1.00], ## Sigma fit
                                  # 'errOneStrip': [ 1.00, 00.47, 00.40, 00.39, 00.40,  1.00,  1.00}],## Sigma fit
                                    'errOneStrip': [ 1.00,  1.00,  1.00,  1.00,  1.00,  1.00,  1.00]},
    "EIC_W1_1cm_500up_200uw_255V": {'resOneStrip': [-1.00, 76.99, 81.69, 79.00, 82.88, 84.76, -1.00],
                                    'errOneStrip': [ 1.00, 00.23, 00.19, 00.10, 00.15, 00.16,  1.00]},
    "EIC_W2_1cm_500up_100uw_220V": {'resOneStrip': [-1.00, 66.17, 68.40, 66.86, 68.28, 72.04, -1.00], ## Std Dev
                                  # 'resOneStrip': [-1.00, 59.17, 63.30, 61.23, 64.21, 69.26, -1.00], ## Sigma fit
                                  # 'errOneStrip': [ 1.00, 00.32, 00.30, 00.20, 00.17,  0.19,  1.00]},## Sigma fit
                                    'errOneStrip': [ 1.00,  1.00,  1.00,  1.00,  1.00,  1.00,  1.00]},
    "EIC_W1_2p5cm_500up_200uw_215V": {'resOneStrip': [-1.00, 76.99, 81.69, 79.00, 82.88, 84.76, -1.00],
                                      'errOneStrip': [ 1.00, 00.23, 00.19, 00.10, 00.15, 00.16,  1.00]},
    "EIC_W1_0p5cm_500up_200uw_1_4_245V": {'resOneStrip': [-1.00, 76.99, 81.69, 79.00, 82.88, 84.76, -1.00],
                                          'errOneStrip': [ 1.00, 00.23, 00.19, 00.10, 00.15, 00.16,  1.00]},
    "HPK_Eb_1cm_80up_45uw": {'resOneStrip': [-1.00, 76.99, 81.69, 79.00, 82.88, 84.76, -1.00],
                             'errOneStrip': [ 1.00, 00.23, 00.19, 00.10, 00.15, 00.16,  1.00]},
    "BNL2021_22_medium_150up_80uw_285V": {'resOneStrip': [-1.00, 76.99, 81.69, 79.00, 82.88, 84.76, -1.00],
                                          'errOneStrip': [ 1.00, 00.23, 00.19, 00.10, 00.15, 00.16,  1.00]},
}

### 2023 Sensors' information dictionaries
# Dataset_name: {'sensor': <name>, 'pitch': [micron], 'stripWidth': [micron], "BV": [V], "length": [mm]},
sensorsGeom2023 = { "BNL_50um_1cm_450um_W3051_2_2": {'sensor': "BNL_50um_1cm_450um_W3051", 'pitch': 500, 'stripWidth': 50, "BV": 170, "length": 10.0},
                    "BNL_50um_1cm_400um_W3051_1_4": {'sensor': "BNL_50um_1cm_400um_W3051", 'pitch': 500, 'stripWidth': 100, "BV": 160, "length": 10.0},
                    "BNL_50um_1cm_450um_W3052_2_4": {'sensor': "BNL_50um_1cm_450um_W3052", 'pitch': 500, 'stripWidth': 50, "BV": 185, "length": 10.0},
                    "BNL_20um_1cm_400um_W3074_1_4": {'sensor': "BNL_20um_1cm_400um_W3074", 'pitch': 500, 'stripWidth': 100, "BV": 95, "length": 10.0},
                    "BNL_20um_1cm_400um_W3075_1_2": {'sensor': "BNL_20um_1cm_400um_W3075", 'pitch': 500, 'stripWidth': 100, "BV": 80, "length": 10.0},
                    "BNL_20um_1cm_450um_W3074_2_1": {'sensor': "BNL_20um_1cm_450um_W3074", 'pitch': 500, 'stripWidth': 50, "BV": 95, "length": 10.0},
                    "BNL_20um_1cm_450um_W3075_2_4": {'sensor': "BNL_20um_1cm_450um_W3075", 'pitch': 500, 'stripWidth': 50, "BV": 80, "length": 10.0},
                    "BNL_50um_2p5cm_mixConfig1_W3051_1_4": {'sensor': "BNL_50um_2p5cm_mixConfig1_W3051", 'pitch': 500, 'stripWidth': 100, "BV": 170, "length": 25.0},
                    "BNL_50um_2p5cm_mixConfig2_W3051_1_4": {'sensor': "BNL_50um_2p5cm_mixConfig2_W3051", 'pitch': 500, 'stripWidth': 50, "BV": 170, "length": 25.0},
                    "HPK_20um_500x500um_2x2pad_E600_FNAL": {'sensor': "HPK_20um_2x2pad", 'pitch': 500, 'stripWidth': 500, "BV": 105, "length": 0.5},
                    "HPK_30um_500x500um_2x2pad_E600_FNAL": {'sensor': "HPK_30um_2x2pad", 'pitch': 500, 'stripWidth': 500, "BV": 140, "length": 0.5},
                    "HPK_50um_500x500um_2x2pad_E600_FNAL": {'sensor': "HPK_50um_2x2pad", 'pitch': 500, 'stripWidth': 500, "BV": 190, "length": 0.5},

                    "HPK_W8_18_2_50T_1P0_500P_100M_C600": {'sensor': "HPK_W8_18_2_50T_100M_C600", 'pitch': 500, 'stripWidth': 100, "BV": 208, "length": 10.0},
                    
                    "HPK_W8_17_2_50T_1P0_500P_50M_C600": {'sensor': "HPK_W8_17_2_50T_50M_C600", 'pitch': 500, 'stripWidth': 50, "BV": 206, "length": 10.0},
                    "HPK_W8_17_2_50T_1P0_500P_50M_C600_200V": {'sensor': "HPK_W8_17_2_50T_50M_C600", 'pitch': 500, 'stripWidth': 50, "BV": 200, "length": 10.0},

                    "HPK_W4_17_2_50T_1P0_500P_50M_C240": {'sensor': "HPK_W4_17_2_50T_1P0_500P_50M_C240", 'pitch': 500, 'stripWidth': 50, "BV": 204, "length": 10.0},

                    "HPK_W5_17_2_50T_1P0_500P_50M_E600": {'sensor': "HPK_W5_17_2_50T_1P0_500P_50M_E600", 'pitch': 500, 'stripWidth': 50, "BV": 190, "length": 10.0},
                    "HPK_W5_17_2_50T_1P0_500P_50M_E600_188V": {'sensor': "HPK_W5_17_2_50T_1P0_500P_50M_E600", 'pitch': 500, 'stripWidth': 50, "BV": 188, "length": 10.0},
                    "HPK_W5_17_2_50T_1P0_500P_50M_E600_186V": {'sensor': "HPK_W5_17_2_50T_1P0_500P_50M_E600", 'pitch': 500, 'stripWidth': 50, "BV": 186, "length": 10.0},
                    "HPK_W5_17_2_50T_1P0_500P_50M_E600_192V": {'sensor': "HPK_W5_17_2_50T_1P0_500P_50M_E600", 'pitch': 500, 'stripWidth': 50, "BV": 192, "length": 10.0},
                    "HPK_W5_17_2_50T_1P0_500P_50M_E600_194V": {'sensor': "HPK_W5_17_2_50T_1P0_500P_50M_E600", 'pitch': 500, 'stripWidth': 50, "BV": 194, "length": 10.0},
                    
                    "HPK_W9_15_2_20T_1P0_500P_50M_E600": {'sensor': "HPK_W9_15_2_20T_1P0_500P_50M_E600", 'pitch': 500, 'stripWidth': 50, "BV": 114, "length": 10.0},
                    "HPK_W2_3_2_50T_1P0_500P_50M_E240": {'sensor': "HPK_W2_3_2_50T_1P0_500P_50M_E240", 'pitch': 500, 'stripWidth': 50, "BV": 180, "length": 10.0},
                    "HPK_W9_14_2_20T_1P0_500P_100M_E600": {'sensor': "HPK_W9_14_2_20T_1P0_500P_100M_E600", 'pitch': 500, 'stripWidth': 100, "BV": 112, "length": 10.0},
                    "HPK_KOJI_50T_1P0_80P_60M_E240": {'sensor': "HPK_KOJI_50T_1P0_80P_60M_E240", 'pitch': 80, 'stripWidth': 60, "BV": 190, "length": 10.0},
                    "HPK_KOJI_20T_1P0_80P_60M_E240": {'sensor': "HPK_KOJI_20T_1P0_80P_60M_E240", 'pitch': 80, 'stripWidth': 60, "BV": 112, "length": 10.0},
}

# NEED TO BE UPDATED! ONLY PLACEHOLDERS TO MAKE PAPER_PLOTS MACROS RUN
# 'position_oneStrip': Std Dev from fit, 'position_oneStrip_E': Statistical error from fit, 'position_oneStripRMS': RMS WITH OnMetal cut,
# 'position_oneStrip_StdDev': RMS WITHOUT OnMetal cut (This is the value used in the paper)
resolutions2023 = {
    "BNL_50um_1cm_450um_W3051_2_2_170V": {'position_oneStrip'  : 0.00, 'position_oneStrip_E': 0.00, 'position_oneStripRMS': 0.00,
                                        'position_oneStrip_StdDev': 0.00,
                                        'position_twoStrip'  : 0.00, 'position_twoStrip_E': 0.00,
                                        'efficiency_oneStrip': 0.00, 'efficiency_twoStrip' : 0.00},
    "BNL_50um_1cm_400um_W3051_1_4_160V": {'position_oneStrip'  : 0.00, 'position_oneStrip_E': 0.00, 'position_oneStripRMS': 0.00,
                                        'position_oneStrip_StdDev': 0.00,
                                        'position_twoStrip'  : 0.00, 'position_twoStrip_E': 0.00,
                                        'efficiency_oneStrip': 0.00, 'efficiency_twoStrip' : 0.00},
    "BNL_50um_1cm_450um_W3052_2_4_185V": {'position_oneStrip'  : 0.00, 'position_oneStrip_E': 0.00, 'position_oneStripRMS': 0.00,
                                        'position_oneStrip_StdDev': 0.00,
                                        'position_twoStrip'  : 0.00, 'position_twoStrip_E': 0.00,
                                        'efficiency_oneStrip': 0.00, 'efficiency_twoStrip' : 0.00},
    "BNL_20um_1cm_400um_W3074_1_4_95V": {'position_oneStrip'  : 0.00, 'position_oneStrip_E': 0.00, 'position_oneStripRMS': 0.00,
                                        'position_oneStrip_StdDev': 0.00,
                                        'position_twoStrip'  : 0.00, 'position_twoStrip_E': 0.00,
                                        'efficiency_oneStrip': 0.00, 'efficiency_twoStrip' : 0.00},
    "BNL_20um_1cm_400um_W3075_1_2_80V": {'position_oneStrip'  : 0.00, 'position_oneStrip_E': 0.00, 'position_oneStripRMS': 0.00,
                                        'position_oneStrip_StdDev': 0.00,
                                        'position_twoStrip'  : 0.00, 'position_twoStrip_E': 0.00,
                                        'efficiency_oneStrip': 0.00, 'efficiency_twoStrip' : 0.00},
    "BNL_20um_1cm_450um_W3074_2_1_95V": {'position_oneStrip'  : 0.00, 'position_oneStrip_E': 0.00, 'position_oneStripRMS': 0.00,
                                        'position_oneStrip_StdDev': 0.00,
                                        'position_twoStrip'  : 0.00, 'position_twoStrip_E': 0.00,
                                        'efficiency_oneStrip': 0.00, 'efficiency_twoStrip' : 0.00},
    "BNL_20um_1cm_450um_W3075_2_4_80V": {'position_oneStrip'  : 0.00, 'position_oneStrip_E': 0.00, 'position_oneStripRMS': 0.00,
                                        'position_oneStrip_StdDev': 0.00,
                                        'position_twoStrip'  : 0.00, 'position_twoStrip_E': 0.00,
                                        'efficiency_oneStrip': 0.00, 'efficiency_twoStrip' : 0.00},
    "BNL_50um_2p5cm_mixConfig1_W3051_1_4_170V": {'position_oneStrip'  : 0.00, 'position_oneStrip_E': 0.00, 'position_oneStripRMS': 0.00,
                                        'position_oneStrip_StdDev': 0.00,
                                        'position_twoStrip'  : 0.00, 'position_twoStrip_E': 0.00,
                                        'efficiency_oneStrip': 0.00, 'efficiency_twoStrip' : 0.00},
    "BNL_50um_2p5cm_mixConfig2_W3051_1_4_170V": {'position_oneStrip'  : 0.00, 'position_oneStrip_E': 0.00, 'position_oneStripRMS': 0.00,
                                        'position_oneStrip_StdDev': 0.00,
                                        'position_twoStrip'  : 0.00, 'position_twoStrip_E': 0.00,
                                        'efficiency_oneStrip': 0.00, 'efficiency_twoStrip' : 0.00},
    "HPK_20um_500x500um_2x2pad_E600_FNAL_105V": {'position_oneStrip'  : 0.00, 'position_oneStrip_E': 0.00, 'position_oneStripRMS': 0.00,
                                        'position_oneStrip_StdDev': 0.00,
                                        'position_twoStrip'  : 0.00, 'position_twoStrip_E': 0.00,
                                        'efficiency_oneStrip': 0.00, 'efficiency_twoStrip' : 0.00},
    "HPK_30um_500x500um_2x2pad_E600_FNAL_140V": {'position_oneStrip'  : 0.00, 'position_oneStrip_E': 0.00, 'position_oneStripRMS': 0.00,
                                        'position_oneStrip_StdDev': 0.00,
                                        'position_twoStrip'  : 0.00, 'position_twoStrip_E': 0.00,
                                        'efficiency_oneStrip': 0.00, 'efficiency_twoStrip' : 0.00},
    "HPK_50um_500x500um_2x2pad_E600_FNAL_190V": {'position_oneStrip'  : 0.00, 'position_oneStrip_E': 0.00, 'position_oneStripRMS': 0.00,
                                        'position_oneStrip_StdDev': 0.00,
                                        'position_twoStrip'  : 0.00, 'position_twoStrip_E': 0.00,
                                        'efficiency_oneStrip': 0.00, 'efficiency_twoStrip' : 0.00},

    "HPK_W8_18_2_50T_1P0_500P_100M_C600_208V": {'position_oneStrip'  : 0.00, 'position_oneStrip_E': 0.00, 'position_oneStripRMS': 0.00,
                                        'position_oneStrip_StdDev': 0.00,
                                        'position_twoStrip'  : 0.00, 'position_twoStrip_E': 0.00,
                                        'efficiency_oneStrip': 0.00, 'efficiency_twoStrip' : 0.00},
    # "HPK_W8_17_2_50T_1P0_500P_50M_C600":,
    # "HPK_W8_17_2_50T_1P0_500P_50M_C600_200V":,
    "HPK_W4_17_2_50T_1P0_500P_50M_C240_204V": {'position_oneStrip'  : 0.00, 'position_oneStrip_E': 0.00, 'position_oneStripRMS': 0.00,
                                        'position_oneStrip_StdDev': 0.00,
                                        'position_twoStrip'  : 0.00, 'position_twoStrip_E': 0.00,
                                        'efficiency_oneStrip': 0.00, 'efficiency_twoStrip' : 0.00},
    # "HPK_W5_17_2_50T_1P0_500P_50M_E600":,
    # "HPK_W5_17_2_50T_1P0_500P_50M_E600_188V":,
    # "HPK_W5_17_2_50T_1P0_500P_50M_E600_186V":,
    # "HPK_W5_17_2_50T_1P0_500P_50M_E600_192V":,
    # "HPK_W5_17_2_50T_1P0_500P_50M_E600_194V":,
    "HPK_W9_15_2_20T_1P0_500P_50M_E600_114V": {'position_oneStrip'  : 0.00, 'position_oneStrip_E': 0.00, 'position_oneStripRMS': 0.00,
                                          'position_oneStrip_StdDev': 0.00,
                                          'position_twoStrip'  : 0.00, 'position_twoStrip_E': 0.00,
                                          'efficiency_oneStrip': 0.00, 'efficiency_twoStrip' : 0.00},
    "HPK_W2_3_2_50T_1P0_500P_50M_E240_180V": {'position_oneStrip'  : 0.00, 'position_oneStrip_E': 0.00, 'position_oneStripRMS': 0.00,
                                         'position_oneStrip_StdDev': 0.00,
                                         'position_twoStrip'  : 0.00, 'position_twoStrip_E': 0.00,
                                         'efficiency_oneStrip': 0.00, 'efficiency_twoStrip' : 0.00},
    "HPK_W9_14_2_20T_1P0_500P_100M_E600_112V": {'position_oneStrip'  : 0.00, 'position_oneStrip_E': 0.00, 'position_oneStripRMS': 0.00,
                                           'position_oneStrip_StdDev': 0.00,
                                           'position_twoStrip'  : 0.00, 'position_twoStrip_E': 0.00,
                                           'efficiency_oneStrip': 0.00, 'efficiency_twoStrip' : 0.00},
    "HPK_KOJI_50T_1P0_80P_60M_E240_190V": {'position_oneStrip'  : 0.00, 'position_oneStrip_E': 0.00, 'position_oneStripRMS': 0.00,
                                      'position_oneStrip_StdDev': 0.00,
                                      'position_twoStrip'  : 0.00, 'position_twoStrip_E': 0.00,
                                      'efficiency_oneStrip': 0.00, 'efficiency_twoStrip' : 0.00},
    "HPK_KOJI_20T_1P0_80P_60M_E240_112V": {'position_oneStrip'  : 0.00, 'position_oneStrip_E': 0.00, 'position_oneStripRMS': 0.00,
                                      'position_oneStrip_StdDev': 0.00,
                                      'position_twoStrip'  : 0.00, 'position_twoStrip_E': 0.00,
                                      'efficiency_oneStrip': 0.00, 'efficiency_twoStrip' : 0.00},
}

resolutions2023OneStripChannel = {
"BNL_50um_1cm_450um_W3051_2_2_170V": {  'resOneStrip': [-1.00, -1.00, -1.00, -1.00, -1.00, -1.00, -1.00],  ## Std Dev
                                        'errOneStrip': [ 1.00,  1.00,  1.00,  1.00,  1.00,  1.00,  1.00]}, ## Sigma fit
"BNL_50um_1cm_400um_W3051_1_4_160V": {  'resOneStrip': [-1.00, -1.00, -1.00, -1.00, -1.00, -1.00, -1.00],  ## Std Dev
                                        'errOneStrip': [ 1.00,  1.00,  1.00,  1.00,  1.00,  1.00,  1.00]}, ## Sigma fit
"BNL_50um_1cm_450um_W3052_2_4_185V": {  'resOneStrip': [-1.00, -1.00, -1.00, -1.00, -1.00, -1.00, -1.00],  ## Std Dev
                                        'errOneStrip': [ 1.00,  1.00,  1.00,  1.00,  1.00,  1.00,  1.00]}, ## Sigma fit
"BNL_20um_1cm_400um_W3074_1_4_95V": {   'resOneStrip': [-1.00, -1.00, -1.00, -1.00, -1.00, -1.00, -1.00],  ## Std Dev
                                        'errOneStrip': [ 1.00,  1.00,  1.00,  1.00,  1.00,  1.00,  1.00]}, ## Sigma fit
"BNL_20um_1cm_400um_W3075_1_2_80V": {   'resOneStrip': [-1.00, -1.00, -1.00, -1.00, -1.00, -1.00, -1.00],  ## Std Dev
                                        'errOneStrip': [ 1.00,  1.00,  1.00,  1.00,  1.00,  1.00,  1.00]}, ## Sigma fit
"BNL_20um_1cm_450um_W3074_2_1_95V": {   'resOneStrip': [-1.00, -1.00, -1.00, -1.00, -1.00, -1.00, -1.00],  ## Std Dev
                                        'errOneStrip': [ 1.00,  1.00,  1.00,  1.00,  1.00,  1.00,  1.00]}, ## Sigma fit
"BNL_20um_1cm_450um_W3075_2_4_80V": {   'resOneStrip': [-1.00, -1.00, -1.00, -1.00, -1.00, -1.00, -1.00],  ## Std Dev
                                        'errOneStrip': [ 1.00,  1.00,  1.00,  1.00,  1.00,  1.00,  1.00]}, ## Sigma fit
"BNL_50um_2p5cm_mixConfig1_W3051_1_4_170V": {   'resOneStrip': [-1.00, -1.00, -1.00, -1.00, -1.00, -1.00, -1.00],  ## Std Dev
                                                'errOneStrip': [ 1.00,  1.00,  1.00,  1.00,  1.00,  1.00,  1.00]}, ## Sigma fit
"BNL_50um_2p5cm_mixConfig2_W3051_1_4_170V": {   'resOneStrip': [-1.00, -1.00, -1.00, -1.00, -1.00, -1.00, -1.00],  ## Std Dev
                                                'errOneStrip': [ 1.00,  1.00,  1.00,  1.00,  1.00,  1.00,  1.00]}, ## Sigma fit
"HPK_20um_500x500um_2x2pad_E600_FNAL_105V": {   'resOneStrip': [-1.00, -1.00, -1.00, -1.00, -1.00, -1.00, -1.00],  ## Std Dev
                                                'errOneStrip': [ 1.00,  1.00,  1.00,  1.00,  1.00,  1.00,  1.00]}, ## Sigma fit
"HPK_30um_500x500um_2x2pad_E600_FNAL_140V": {   'resOneStrip': [-1.00, -1.00, -1.00, -1.00, -1.00, -1.00, -1.00],  ## Std Dev
                                                'errOneStrip': [ 1.00,  1.00,  1.00,  1.00,  1.00,  1.00,  1.00]}, ## Sigma fit
"HPK_50um_500x500um_2x2pad_E600_FNAL_190V": {   'resOneStrip': [-1.00, -1.00, -1.00, -1.00, -1.00, -1.00, -1.00],  ## Std Dev
                                                'errOneStrip': [ 1.00,  1.00,  1.00,  1.00,  1.00,  1.00,  1.00]}, ## Sigma fit

"HPK_W8_18_2_50T_1P0_500P_100M_C600_208V": {'resOneStrip': [-1.00, -1.00, -1.00, -1.00, -1.00, -1.00, -1.00],  ## Std Dev
                                       'errOneStrip': [ 1.00,  1.00,  1.00,  1.00,  1.00,  1.00,  1.00]}, ## Sigma fit
# "HPK_W8_17_2_50T_1P0_500P_50M_C600":,
# "HPK_W8_17_2_50T_1P0_500P_50M_C600_200V":,
"HPK_W4_17_2_50T_1P0_500P_50M_C240_204V": {'resOneStrip': [-1.00, -1.00, -1.00, -1.00, -1.00, -1.00, -1.00],  ## Std Dev
                                      'errOneStrip': [ 1.00,  1.00,  1.00,  1.00,  1.00,  1.00,  1.00]}, ## Sigma fit
# "HPK_W5_17_2_50T_1P0_500P_50M_E600":,
# "HPK_W5_17_2_50T_1P0_500P_50M_E600_188V":,
# "HPK_W5_17_2_50T_1P0_500P_50M_E600_186V":,
# "HPK_W5_17_2_50T_1P0_500P_50M_E600_192V":,
# "HPK_W5_17_2_50T_1P0_500P_50M_E600_194V":,
"HPK_W9_15_2_20T_1P0_500P_50M_E600_114V": {'resOneStrip': [-1.00, -1.00, -1.00, -1.00, -1.00, -1.00, -1.00],  ## Std Dev
                                      'errOneStrip': [ 1.00,  1.00,  1.00,  1.00,  1.00,  1.00,  1.00]}, ## Sigma fit
"HPK_W2_3_2_50T_1P0_500P_50M_E240_180V": {'resOneStrip': [-1.00, -1.00, -1.00, -1.00, -1.00, -1.00, -1.00],  ## Std Dev
                                          'errOneStrip': [ 1.00,  1.00,  1.00,  1.00,  1.00,  1.00,  1.00]}, ## Sigma fit
"HPK_W9_14_2_20T_1P0_500P_100M_E600_112V": {'resOneStrip': [-1.00, -1.00, -1.00, -1.00, -1.00, -1.00, -1.00],  ## Std Dev
                                       'errOneStrip': [ 1.00,  1.00,  1.00,  1.00,  1.00,  1.00,  1.00]}, ## Sigma fit
"HPK_KOJI_50T_1P0_80P_60M_E240_190V": {'resOneStrip': [-1.00, -1.00, -1.00, -1.00, -1.00, -1.00, -1.00],  ## Std Dev
                                  'errOneStrip': [ 1.00,  1.00,  1.00,  1.00,  1.00,  1.00,  1.00]}, ## Sigma fit
"HPK_KOJI_20T_1P0_80P_60M_E240_112V": {'resOneStrip': [-1.00, -1.00, -1.00, -1.00, -1.00, -1.00, -1.00],  ## Std Dev
                                  'errOneStrip': [ 1.00,  1.00,  1.00,  1.00,  1.00,  1.00,  1.00]}, ## Sigma fit
}


