'''
Code to load the data and create the figures and tables in the main text for 'A Measure of Congressional Committee Influence'
'''
# Setup
import matplotlib.pyplot as plt
import matplotlib
import pylab
from matplotlib import cm
from collections import OrderedDict
import pandas as pd
import pickle
import csv
import statistics


# Plot parameters
cmaps = OrderedDict()

pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 100)

matplotlib.style.use('grayscale')
plt.style.use('grayscale')
params = {
    'axes.grid': True,
    'grid.alpha': .5,
    'grid.linewidth': .2,
    'font.family': 'serif',
    #'figure.autolayout': True,
    #'figure.constrained_layout.use': True,
    'font.size': 12,
    'font.weight': 200,
    'axes.titlesize': 'small',
    'axes.labelsize': 'x-small',
    'xtick.labelsize': 'xx-small',
    'ytick.labelsize': 'xx-small',
    'legend.fontsize': 'xx-small',
    'figure.dpi': 600,
    'lines.markersize': 2,
    'lines.linewidth': 1,
    'axes.xmargin': .005,
    'axes.ymargin': .005,
    'axes.titlepad': 2,
    'axes.labelpad': 1,
    'axes.linewidth': .5,
    'lines.antialiased': True,
    'patch.antialiased': True,
    'xtick.major.size': .5,
    'xtick.minor.size': .025,
    'xtick.major.pad': .5,
    'xtick.minor.pad': .5,
    'ytick.major.size': .5,
    'ytick.minor.size': .025,
    'ytick.major.pad': .5,
    'ytick.minor.pad': .5,
    'legend.frameon': False,
    'legend.columnspacing': .3,
    'legend.borderaxespad': .05,
    'legend.handlelength': 1,
    'legend.borderpad' : .3,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': .02
}
plt.rcParams.update(params)
pylab.rcParams.update(params)
matplotlib.rcParams.update(params)

plt.rcParams["figure.dpi"] = 300

# Functions
def update_col_names(cross_tab):
    """Updates the column names to have a uniform style across plots.

    Args:
        cross_tab (pandas.DataFrame): The data frame whose columns attribute is to be updated.
    """
    new_name_dict = dict()
    for col in cross_tab.columns.values:
        new_name_dict[col] = col.replace('_', ' ').title()
    cross_tab = cross_tab.rename(columns=new_name_dict)
    return cross_tab


def export_cross_tab_table(cross_tab, file_name):
    table_dir = 'C:/Users/Ryan/Documents/Research/HTML Parse 2024/Data/Committee Power/'
    out_file = table_dir + file_name + '.csv'
    with open(out_file, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        headers = [cross_tab.index.name.upper()] + cross_tab.columns.values.tolist()
        writer.writerow(headers)
        for tab_index, tab_row in cross_tab.iterrows():
            writer.writerow([tab_row.name] + tab_row.tolist())

# Import Data
laws = pd.read_csv('..data/laws.csv')
laws_2 = pd.read_csv('..data/laws_2.csv')
data = pd.read_csv('..data/committee_data.csv')


# Code Conversions
## Convert Comparative Agendas Project (CAP [formerly PAP]) codes to text
pap_conv_dict = {
    1: 'Econ.',
    2: 'Rights',
    3: 'Health',
    4: 'Ag.',
    5: 'Labor',
    6: 'Ed.',
    7: 'Env.',
    8: 'Energy',
    9: 'Imm.',
    10: 'Trans.',
    12: 'Crime',
    13: 'Welfare',
    14: 'Housing',
    15: 'Comm.',
    16: 'Defense',
    17: 'Tech.',
    18: 'Trade',
    19: 'Int\'l.',
    20: 'Op.',
    21: 'Lands',
    99: 'Misc.'
}

pap_conv_dict_2 = dict()
for key in pap_conv_dict.keys():
    pap_conv_dict_2[str(key)] = pap_conv_dict[key]
    pap_conv_dict_2[int(key)] = pap_conv_dict[key]


## Convert numerical Stewart committee codes to names
stewart_to_committee = {
    102: 'Agriculture',
    104: 'Appropriations',
    106: 'Armed Services',
    113: 'Financial Srvcs',
    115: 'Budget',
    120: 'D.C.',
    124: 'Education',
    128: 'Energy',
    134: 'Int\'l Affrs',
    138: 'Reform',
    142: 'Admin',
    156: 'Judiciary',
    160: 'Mrchnt Marine',
    164: 'Resources',
    168: 'P. O.',
    173: 'Public Works',
    176: 'Rules',
    182: 'Science',
    184: 'Business',
    186: 'Conduct',
    242: 'Intelligence',
    251: 'Hmlnd Security',
    192: 'VA',
    196: 'Ways & Means',
    0: 'None'
}

# Figure 1
ct = pd.crosstab(index=data[data['year'] % 2 == 0]['congress'], columns=data[data['year'] % 2 == 0]['pap'])

plot_value = ct.columns.name.replace('_', ' ').title()
ct.columns.name = plot_value
# ct = update_col_names(ct)
ct = ct.rename(columns=pap_conv_dict)
index_type = ct.index.name.replace('_', ' ').title()
name = '%s by %s' % (plot_value, index_type)
linestyles = ['-', '--', '-.', ':', '.-', '--', '<-.', '>:', '^-', 's--', '+-.', 'x:', 'd-', '1--', '2-.', '3:',
              'h-', 'p--', 'D-.', '|:', '-']
ct.plot(xticks=list(range(103, 116)), figsize=(12, 12), colormap='tab20b', style=linestyles)
plt.xlim((102.5, 115.5))
plt.ylim((0, 11000))
plt.ylabel('Number of Sections')
plt.xlabel(index_type)
# plt.title(name)
plt.legend(loc='upper center', fontsize='small', ncol=7, prop={'size': 8})
#plt.tight_layout()
plt.savefig(save_file + name.replace(' ', '') + '.png')
#export_cross_tab_table(cross_tab=ct, file_name=name)


# Figure 2
ct = pd.crosstab(index=laws_2['Congress'], columns=laws_2['Committee'])
ct = ct.rename(columns=stewart_to_committee)


col_ord_no_pcans = ct_pca.iloc[-1,:].sort_values(ascending = False).index[0:-4]
linestyles = ['-', '--', '-.', ':', '.-', '--', '<-.', '>:', '^-', 's--', '+-.', 'x:', 'd-', '1--', '2-.', '3:',
              'h-', 'p--', 'D-.', '|:', '-']


ct_pca.loc[:,col_ord_no_pcans].plot(kind='line', stacked=False, sort_columns=True,
                        figsize=(8, 8), colormap='tab20b', style=linestyles,
                        legend='reverse')
plt.legend(loc='upper left', fontsize='xx-small', ncol=3, frameon=False, prop={'size': 8})
plt.ylim((0, 8000))
plt.xlim((79, 116))
plt.ylabel('Count')
plt.xlabel('Congress')
name = 'Committee Counts (count)'
plt.tight_layout()
plt.savefig(save_file + name.replace(' ', '') + 'Style1 NO PC ANS.png')


# Figure 3
ct = pd.crosstab(index=laws[laws['ANS'] != 'PC ANS']['Committee'], columns=laws['PAP'])
ct = ct.rename(index=stewart_to_committee, columns=pap_conv_dict_2)
ct.iloc[1:,:].plot(kind='bar', stacked=True, sort_columns=True, rot=90, figsize=(5, 5), colormap='tab20b')
plt.ylim((0,11000))
plt.ylabel('Section Committee Count')
plt.xlabel('Committee')
plt.legend(loc="upper left", ncol=7, frameon=False)
plt.tight_layout()
name = 'Committee PAP Count No PC ANS'
plt.savefig(save_file + name.replace(' ', '') + '.png')
export_cross_tab_table(cross_tab=ct, file_name=name)


# Table 1
words = data[data['year'] % 2 == 0].groupby(['congress'])['word_count'].sum()

ct = pd.crosstab(index=laws_2['Congress'], columns=laws_2['Committee'])
ct_no_pcnas = pd.crosstab(index=laws_2[laws_2['ANS'] != 'PC ANS']['Congress'], columns=laws_2[laws_2['ANS'] != 'PC ANS']['Committee'])

totwords104_no_pcnas = laws_2[laws_2['Congress'] == 104][laws_2['ANS'] != 'PC ANS'].groupby(['Committee'])['Work Count 104'].sum()
totwords115_no_pcnas = laws_2[laws_2['Congress'] == 115][laws_2['ANS'] != 'PC ANS'].groupby(['Committee'])['Word Count 115'].sum()

word_prop104_no_pcnas  = totwords104_no_pcnas / words[104]
word_prop115_no_pcnas = totwords115_no_pcnas / words[115]


out_table = pd.DataFrame(
    data={'Prop. in 104th': word_prop104_no_pcnas,
          'Prop. in 115th': word_prop115_no_pcnas,
          })
out_table = out_table.iloc[1:,:]
out_table['104th Rank'] = out_table['Prop. in 104th'].rank(ascending=False)
out_table['105th Rank'] = out_table['Prop. in 115th'].rank(ascending=False)

out_table = out_table.loc[out_table.iloc[:,-1].sort_values(ascending = True).index,:]

gw = {
    102: '16',
    104: '3',
    106: '7',
    113: '6',
    115: '11',
    124: '15',
    128: '2',
    134: '5',
    138: '14',
    142: '10',
    156: '8',
    164: '13',
    173: '12',
    176: '4',
    182: '18',
    184: '20',
    #186: '9',
    242: 'NA',
    251: '19',
    192: '17',
    196: '1'
}
out_table.loc[gw.keys(), 'Grosewort'] = [v for v in gw.values()]
out_table = out_table.rename(index=stewart_to_committee)
name = 'CommitteeANSInfoNOPCANS'
out_table = round(out_table, 4)
export_cross_tab_table(cross_tab=out_table, file_name=name)
