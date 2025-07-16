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