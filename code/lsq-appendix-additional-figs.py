##################################################
# A Mesure of Congressional Committee Influence
# Legislative Studies Quarterly
##################################################

'''
The following code is for Figures 1, 2, 4, 5, and 6 in Section 8 ("Additional Figures") in the Supplemental Appendix 
as well as the code to create the tables not already provided in the main text code.
The data are pivoted from wide to long format and then plotted using facet plots.
'''

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd 

# Read in figure data files
# CAP counts by congress data
df1 = pd.read_csv("CAPbyCong.csv")

# Committee counts by congress data
df2 = pd.read_csv("CommCountsbyCong.csv")

### function for turning data from wide to long for figures
def melt_long(df, id_vars, value_vars=None, var_name='variable', value_name='value', new_column_names=None):
    """
    takes df, shifts data from wide to long, renames columns.

    df: df to pivot
    id_vars: columns to use as id vars
    value_vars: columns to unpivot; if not specified, uses all columns that are not set as id_vars
    var_name: name to use for the 'variable' column; default is 'variable'
    value_name: name to use for the 'value' column; default is 'value'
    new_column_names: dict applies original column names to new column names
    return: A df in long format with renamed columns
    """
    df_long = df.melt(id_vars=id_vars, value_vars=value_vars, var_name=var_name, value_name=value_name)

    if new_column_names:
        df_long = df_long.rename(columns=new_column_names)

    return df_long

# Pivot df1 for fig 1b
df1_long = melt_long(
    df=df1,
    id_vars=['CONGRESS'],
    var_name='Category',
    value_name='Count',
    new_column_names={"CONGRESS": "Congress", "Value": "Count", "Category": "CAP"}
)

print(df1_long.head())

# Pivot df2 for fig 2
df2_long = melt_long(
    df=df2,
    id_vars=['CONGRESS'],
    var_name='Category',
    value_name='Count',
    new_column_names={"CONGRESS": "Congress", "Value": "Count", "Category": "Committee"}
)

print(df2_long.head())

### function for facet plots
def plot_facet_fig(df, x_axis, y_axis, fac_col, col_wrap=6, sharey=True, sharex=False):
    """
    plots a facetgrid of line plots from a long df.

    df: long formatted df of data
    x_axis: column used for x-axis
    y_axis: column used for y-axis
    fac_col: column used for faceting grid
    col_wrap: max number of facet columns; default is 6
    sharey: if y-axis will be shared among facets; default is True
    sharey: if x-axis will be shared among facets; default is False
    """

    sns.set_theme(style="whitegrid")
    g = sns.FacetGrid(df, col=fac_col, col_wrap=col_wrap, sharey=sharey, sharex=sharex)
    g = g.map(plt.plot, x_axis, y_axis, marker=' ', color='black')
    g = g.set_titles("{col_name}")
    g = g.fig.tight_layout(w_pad=1)
    plt.show()

# Plot fig 1
plot_facet_fig(df1_long, 'Congress', 'Count', 'CAP')

# Plot fig 2
plot_facet_fig(df2_long, 'Congress', 'Count', 'Committee')

# Appendix Figure 1

rep = []
for sec in CC.combined_sections:
    if sec.created[-1] > 0 and sec.change[-1] in ['was removed', 'Repealed', 'Omitted', 'Mark codified as repealed']:
        #created_cong = convert_year_to_congress(sec.created[-1])
        #created.append(created_cong)
        rep.append(convert_year_to_congress(sec.created[-1]))
r_df = pd.DataFrame(rep, columns=['created'])

creating_com = []
created = []
created_all = []
for sec in CC.combined_sections:
    created_all.append(convert_year_to_congress(sec.created[-1]))
    if isinstance(sec.created[-1], int) and sec.created[-1] > 0 and 'New - Codified' not in sec.match_type and 'Mark codified as repealed' not in sec.match_type:
        #created_cong = convert_year_to_congress(sec.created[-1])
        #created.append(created_cong)
        created.append(convert_year_to_congress(sec.created[-1]))
    elif isinstance(sec.created[0], int) and sec.created[0] > 0 and 'New - Codified' not in sec.match_type and 'Mark codified as repealed' not in sec.match_type:
        #created_cong = convert_year_to_congress(sec.created[-1])
        #created.append(created_cong)
        created.append(convert_year_to_congress(sec.created[0]))
    # if sec.created[-1] > 0 and sec.change[-1] != 'was removed':
    #     #created_cong = convert_year_to_congress(sec.created[-1])
    #     #created.append(created_cong)
    #     created.append(convert_year_to_congress(sec.created[-1]))
    # elif 'New' in sec.change:
    #     #created_cong = convert_year_to_congress(sec.created[-1])
    #     #created.append(created_cong)
    #     add_ind = sec.change.index('New')
    #     created.append(sec.congress[add_ind])
    # elif 'Added' in sec.change:
    #     #created_cong = convert_year_to_congress(sec.created[-1])
    #     #created.append(created_cong)
    #     add_ind = sec.change.index('Added')
    #     created.append(sec.congress[add_ind])
    # elif 'New - Codified' in sec.change:
    #     #created_cong = convert_year_to_congress(sec.created[-1])
    #     #created.append(created_cong)
    #     add_ind = sec.change.index('New - Codified')
    #     created.append(sec.congress[add_ind])
c_df = pd.DataFrame(created, columns=['created'])
created = c_df['created'].value_counts()
created_all = pd.DataFrame(created_all, columns=['created'])['created'].value_counts()

ct = pd.crosstab(index=data[data['change'] != 'was removed'][data['section_type'] != ''][data['year'] % 2 == 0]['congress'],
                 columns=data[data['change'] != 'was removed'][data['section_type'] != ''][data['year'] % 2 == 0]['section_type'])
#data[data['section_type'] == ''].to_csv('no_sec_type.csv')
totals = []
for index, row in ct.iterrows():
    total = sum(row)
    totals.append(total)

created.index.name = 'Year Enacted'
created = created.sort_index()
created_all = created_all.sort_index()
rep = r_df['created'].value_counts()
rep.index.name = 'Year Enacted'
rep = rep.sort_index()

tots = [0]
for ind in range(37, 104):
    try:
        tots.append(tots[-1] + created[ind])
    except KeyError:
        tots.append(tots[-1])
#tots[-1] += rep[103]


matplotlib.rcParams.update({'font.size': 16})
colors = cm.tab20b([1, 2, 4, 5])
fig, ax1 = plt.subplots(figsize=(8, 8), tight_layout=True)
ax1.tick_params(grid_alpha=0)
ax1.margins(0.0025)
ax1.set_xlabel('Enacting Congress')
ax1.set_ylabel('Count')
ax1.set_xmargin(0)
ax1.set_ymargin(0)
ax1.plot(created, color=colors[0], label='Active (Still Enacted)', linestyle='-')
ax1.plot(rep, color=colors[1], label='Inactive (Later Removed)', linestyle='--')
plt.legend(loc='upper left', frameon=False)
plt.xlim((37, 115))
plt.ylim((0, 2550))
#
ax2 = ax1.twinx()
ax2.margins(0.0025)
ax2.tick_params(grid_alpha=0)
ax2.set_ylabel('Total', color='black')  # we already handled the x-label with ax1
ax2.plot(list(range(103, 116)), totals, color=colors[2], label='Total', linestyle='-.')
ax2.plot(list(range(37, 104)), tots[1:], color=colors[3],label='Total (Pre-1994)', linestyle=':')
ax2.tick_params(axis='y', labelcolor='black')
plt.xlim((37, 115))
plt.ylim((0, 55000))
plt.legend(frameon=False, loc='center left', ncol=1)
plt.tight_layout()  # otherwise the right y-label is slightly clipped
plt.tight_layout()
name = 'CreatedbyYear'

plt.savefig(save_file + name + '.png')


# Appendix Figure 2
data = pd.read_csv('..data/committee_data.csv')
matplotlib.rcParams.update({'font.size': 16})

ct = pd.crosstab(index=data['congress'], columns=data['change'], normalize='index')
plot_value = ct.columns.name.replace('_', ' ').title()
ct.columns.name = plot_value
ct = update_col_names(ct)
index_type = ct.index.name.replace('_', ' ').title()
name = '%s by %s (percent)' % (plot_value, index_type)
ct.loc[:,['Amended','New','Repealed','Transferred','Omitted']].plot(sort_columns=False, xticks=list(range(103, 115)), figsize=(6, 5), colormap='tab20b', style=linestyles)
plt.xlim((104, 115))
plt.ylim((0, .06))
plt.ylabel('Proportion of Sections')
plt.xlabel(index_type)
# plt.title(name)
plt.legend(loc=9, frameon=False, ncol=5)
plt.tight_layout()
plt.savefig(save_file + name.replace(' ', '') + '.png')


# Appendix Table 1
## Calculate Values
words = data[data['year'] % 2 == 0].groupby(['congress'])['word_count'].sum()

ct = pd.crosstab(index=data[data['change'] != 'was removed'][data['section_type'] != ''][data['year'] % 2 == 0]['congress'],
                 columns=data[data['change'] != 'was removed'][data['section_type'] != ''][data['year'] % 2 == 0]['section_type'])
totals = []
for index, row in ct.iterrows():
    total = sum(row)
    totals.append(total)


ct = pd.crosstab(index=laws_2['Congress'], columns=laws_2['Committee'])
ct_no_pcnas = pd.crosstab(index=laws_2[laws_2['ANS'] != 'PC ANS']['Congress'], columns=laws_2[laws_2['ANS'] != 'PC ANS']['Committee'])
ct_no_ans = pd.crosstab(index=laws_2[laws_2['ANS'] == 'regular']['Congress'], columns=laws_2[laws_2['ANS'] == 'regular']['Committee'])


count80 = ct.loc[80]
count100 = ct.loc[100]
count104 = ct.loc[104]
count115 = ct.loc[115]
count115_no_pcans = ct_no_pcnas.loc[115]
count115_no_ans = ct_no_ans.loc[115]
count_prop_control80 = ct.loc[80] / sum(ct.loc[80])
count_prop_control100 = ct.loc[100] / sum(ct.loc[100])
count_prop_control104 = ct.loc[104] / sum(ct.loc[104])
count_prop_control115 = ct.loc[115] / sum(ct.loc[115])
count_prop_control115_no_pnans = ct_no_pcnas.loc[115] / sum(ct.loc[115])
count_prop_control115_no_ans = ct_no_ans.loc[115] / sum(ct.loc[115])
count_prop104 = ct.loc[104] / totals[0]
count_prop115 = ct.loc[115] / totals[-1]

#totwords100 = atot_words_section = laws_2[laws_2['Congress'] == 100].groupby(['Committee'])['Word Count'].sum()
totwords104 = laws_2[laws_2['Congress'] == 104].groupby(['Committee'])['Work Count 104'].sum()
totwords104_no_pcnas = laws_2[laws_2['Congress'] == 104][laws_2['ANS'] != 'PC ANS'].groupby(['Committee'])['Work Count 104'].sum()
totwords115 = laws_2[laws_2['Congress'] == 115].groupby(['Committee'])['Word Count 115'].sum()
totwords115_no_pcnas = laws_2[laws_2['Congress'] == 115][laws_2['ANS'] != 'PC ANS'].groupby(['Committee'])['Word Count 115'].sum()
totwords115_no_ans = laws_2[laws_2['Congress'] == 115][laws_2['ANS'] == 'regular'].groupby(['Committee'])['Word Count 115'].sum()

#word_prop_control100 = totwords100 / laws_2[laws_2['Congress'] == 100]['Word Count'].sum()
word_prop_control104 = totwords104 / laws_2[laws_2['Congress'] == 104]['Work Count 104'].sum()
word_prop_control115 = totwords115 / laws_2[laws_2['Congress'] == 115]['Word Count 115'].sum()
word_prop_control104_no_pcnas = totwords104_no_pcnas / laws_2[laws_2['Congress'] == 104]['Work Count 104'].sum()
word_prop_control115_no_pcnas = totwords115_no_pcnas / laws_2[laws_2['Congress'] == 115]['Word Count 115'].sum()
word_prop_control115_no_ans = totwords115_no_ans / laws_2[laws_2['Congress'] == 115]['Word Count 115'].sum()
word_prop104 = totwords104 / words[104]
word_prop104_no_pcnas  = totwords104_no_pcnas / words[104]
word_prop115 = totwords115 / words[115]
word_prop115_no_pcnas = totwords115_no_pcnas / words[115]
word_prop115_no_ans = totwords115_no_ans / words[115]

avg_ref_section115 = laws_2[laws_2['Congress'] == 115].groupby(['Committee'])['Ref'].mean()
avg_ref_section115 = round(avg_ref_section115, 2)

atot_words_section = laws_2[laws_2['Congress'] == 115].groupby(['Committee'])['Word Count 115'].sum()
propr_atot_words_section = atot_words_section / laws_2[laws_2['Congress'] == 115]['Word Count 115'].sum()
propr_atot_words_section = round(propr_atot_words_section, 4)
avg_words_section = laws_2[laws_2['Congress'] == 115].groupby(['Committee'])['Word Count 115'].mean()
avg_words_section = round(avg_words_section, 2)

## Table
out_table = pd.DataFrame(
    data={'Proportion of Words in Controlled Sections (104)': word_prop_control104,
          'Proportion of Words in Controlled Sections (115)': word_prop_control115,
          'Total Sections (104)': count104,
          'Total Sections (115)': count115,
          'Proportion of Controlled (104)': count_prop_control104,
          'Proportion of Controlled (115)': count_prop_control115,
          'Proportion of Sections (104)': count_prop104,
          'Proportion of Sections (115)': count_prop115,
          'Proportion of Words in Sections (104)': word_prop104,
          'Proportion of Words in Sections (115)': word_prop115,
          'Avg Cross Ref (115)': avg_words_section
          })

# Appendix Table 2
out_table = pd.DataFrame(
    data={'Total Sections (115)': count115,
          'Total Sections (115) No PC ANS': count115_no_pcans,
          'Total Sections (115) No ANS': count115_no_ans,
          'Prop Words in Cntrld Sec (115)': word_prop_control115,
          'Prop Words in Cntrld Sec (115) No PC ANS': word_prop_control115_no_pcnas,
          'Prop Words in Cntrld Sec (115) No ANS': word_prop_control115_no_ans,
          'Prop Words (1x count) (115)': word_prop115,
          'Prop Words (1x count) (115) No PC ANS': word_prop115_no_pcnas,
          'Prop Words (1x count) (115) No ANS': word_prop115_no_ans,
          })
name = 'CommitteeANSInfo'
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
    186: '9',
    242: 'NA',
    251: '19',
    192: '17',
    196: '1'
}
out_table.loc[gw.keys(), 'Grosewort'] = [v for v in gw.values()]
out_table = round(out_table, 4)
out_table = out_table.rename(index=stewart_to_committee)
out_table['Total Sections (115) Rank'] = out_table['Total Sections (115)'].rank(ascending=False)
out_table['Total Sections (115) No PC ANS Rank'] = out_table['Total Sections (115) No PC ANS'].rank(ascending=False)
out_table['Total Sections (115) No ANS Rank'] = out_table['Total Sections (115) No ANS'].rank(ascending=False)
out_table['Prop Words in Cntrld Sec (115) Rank'] = out_table['Prop Words in Cntrld Sec (115)'].rank(ascending=False)
out_table['Prop Words in Cntrld Sec (115) No PC ANS Rank'] = out_table['Prop Words in Cntrld Sec (115) No PC ANS'].rank(ascending=False)
out_table['Prop Words in Cntrld Sec (115) No ANS Rank'] = out_table['Prop Words in Cntrld Sec (115) No ANS'].rank(ascending=False)
export_cross_tab_table(cross_tab=out_table, file_name=name)

# Appendix Table 3
## See the 'export_cross_tab_table' section of main text figure 1.


# Appendix Table 4
## See the 'export_cross_tab_table' section of main text figure 2.

# Appendix Table 5
## See the 'export_cross_tab_table' section of main text figure 3.
