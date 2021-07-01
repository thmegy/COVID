import matplotlib.pyplot as plt
import matplotlib.dates
import numpy as np


def plotTests(df, dep, departements, pre, leg, rolling=True):
    '''
    Plot number of positive tests and positivity rate as a function of time.
    '''
    fig, ax = plt.subplots(figsize=(14,10))
    if not rolling:
        rolling_mean = df
        post = ''
    else:
        rolling_mean = df[['P','T']].rolling(7).mean()
        post = ' - Moyenne sur 7 jours'
    converted_dates = matplotlib.dates.datestr2num(df['jour'].to_list())
    ax.plot_date(converted_dates, rolling_mean['P'], '-', label='Tests positifs')
    ax.set_ylabel('Nombre de tests positifs')
    plt.xticks(rotation=45, ha='right')
    ax2 = ax.twinx()
    ax2.plot_date(converted_dates, 100*rolling_mean['P']/rolling_mean['T'], '-', color='red', label='Taux de positivité')
    ax2.set_ylabel('Taux de positivité (%)')
    #ax2.set_yscale('log')
    fig.legend()
    if dep in departements.keys():
        ax.set_title('Suivi des tests COVID-19 {}{}{}'.format(pre[dep], departements[dep], post))
    else:
        ax.set_title('Suivi des tests COVID-19 en {}{}'.format(dep, post))


        

def plotEvol(df, var, dep, departements, pre, leg, rolling=True):
    '''
    Plot evolution of inputed variable as a function of time.
    '''
    if not rolling:
        rolling_mean = df[var]
        post = ''
    else:
        rolling_mean = df[var].rolling(7).mean()
        post = ' - Moyenne sur 7 jours'
    converted_dates = matplotlib.dates.datestr2num(df['jour'].to_list())
    plt.plot_date(converted_dates, rolling_mean, '-')
    plt.ylabel(leg[var])
    plt.xticks(rotation=45, ha='right')
    if dep in departements.keys():
        plt.title('COVID-19: {} {}{}\n{}'.format(leg[var], pre[dep], departements[dep], post))
    else:
        plt.title('COVID-19: {} en {}\n{}'.format(leg[var], dep, post))





def plotTestsVsAge(df, dep, pre, leg, departements):
    '''
    Plot positivity rate as a function of time for each age group, for a given french departement.
    '''
    opts = {'cmap': 'Reds'}
    plt.rcParams['figure.figsize'] = (20, 10)

    age_group = {
                '9' : '0-9',
                '19' : '10-19',
                '29' : '20-29',
                '39' : '30-39',
                '49' : '40-49',
                '59' : '50-59',
                '69' : '60-69',
                '79' : '70-79',
                '89' : '80-89',
                '90' : '>90'
    }

    p_vs_age = []
    for key, val in age_group.items():
        df_tmp = df[df['cl_age90']==int(key)]
        rolling_mean = df_tmp[['P','T']].rolling(7).mean()
        p_vs_age.append( (100*rolling_mean[::-7][::-1].iloc[1:]['P']/rolling_mean[::-7][::-1].iloc[1:]['T']).to_list() )

    dates = df_tmp[::-7][::-1]['jour'].iloc[1:].to_list()
    plt.pcolor(p_vs_age, **opts)
    plt.colorbar()
    xt = plt.xticks(ticks=np.arange(len(dates))+0.5, labels=dates, rotation=45, ha='right')
    ylabels = [val for key, val in age_group.items()]
    yt = plt.yticks(ticks=np.arange(len(ylabels))+0.5, labels=ylabels)
    plt.ylabel('Age')
    if dep in departements.keys():
        plt.title('Taux de positivité des tests COVID-19 {}{} - Moyenne sur 7 jours'.format(pre[dep], departements[dep]))
    else:
        plt.title('Taux de positivité des tests COVID-19 en {} - Moyenne sur 7 jours'.format(dep))
