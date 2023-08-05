import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import ipywidgets as widgets
from ipywidgets import widgets
from ipywidgets import interact


pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

class insights:
    def __init__(self, data):
        self.data = data
        
    def automate_analysis(self):
        bold = '\33[1m'
        not_bold = '\33[m'
        print("\n")
        print("The dataset before cleaning")
        print("The dataset has {} rows and {} columns \n".format(self.data.shape[0],self.data.shape[1]))
        print("\n ---------------------------------------------------------------------\n")
        print(bold + 'Information about the data :' + not_bold)
        print('\n')
        print(self.data.info())
        print("\n ---------------------------------------------------------------------\n")
        
        df = pd.DataFrame(self.data)
        
        print(bold + "Preparing data cleaning ...." + not_bold)
        print('\n')
        self.data = self.data.fillna(0)   # filling the NaN with 0's
        print("Successfully filled the empty spaces and replaced the garbage values to '0'")
        print('\n')
  
        print(bold + "Plots for categorical columns: " + not_bold)
        print('\n')
        
        for i in self.data.columns:
            if len(pd.unique(self.data[i])) > 10:
                if self.data[i].dtypes == object:
                    df = pd.DataFrame((self.data[i].value_counts()/(len(df)*100)).sort_values(ascending=False).head(20))
                    plot1= df.plot(kind='bar',figsize=(12,6))
                    plt.xlabel(i,fontsize=15)
                    plt.ylabel('Frequency',fontsize=15)
                    plt.yscale('log')
                    plt.xticks(fontsize=12)
                    plt.show(plot1)
                    print("\n {} has {} unique values and {} percentage of null values \n".format(i,self.data[i].nunique(),round((self.data[i].isna().sum()/self.data.shape[0])*100,3)))
                    print('\n')
                    print(bold + 'Description of the column :' + not_bold)
                    
                    # descrie data
                    print(df[i].describe(include="all"))
                    print('\n')
                
                
                #for i in self.data.columns:
                if self.data[i].dtypes != object:
                    plt.figure(figsize=(12,9))
                    plot2= sns.displot(self.data[i], bins = 25, kde = False)
                    plt.xlabel(i,fontsize=15)
                    plt.ylabel('Frequency',fontsize=15)
                    plt.yscale('log')
                    plt.xticks(fontsize=12)
                    plt.show(plot2)
                    print("\n {} has {} unique values and {} percentage of null values \n".format(i,self.data[i].nunique(),round((self.data[i].isna().sum()/self.data.shape[0])*100,3)))
                    print('\n')
                    print(bold + 'Description of the column :' + not_bold)
                    
                    # descrie data
                    print(df[i].describe(include="all"))
                    print('\n')
            
            if len(pd.unique(self.data[i])) < 10:
                    df1 = df.groupby([i])[i].count()
                    fig = px.pie(df1, values=i, names=i, title=i)
                    fig.show()
                    print(" {} has {} unique values and {} percentage of null values \n".format(i,self.data[i].nunique(),round((self.data[i].isna().sum()/self.data.shape[0])*100,3)))
                    print(bold + " The unique values are: " + not_bold)
                    for uni in self.data[i]:
                        #print(self.data[i].unique())
                        print(self.data[i].value_counts())
                        break
                    print('\n')
                    print(bold + 'Description of the column :' + not_bold)
                    # descrie data
                    print(df[i].describe(include="all"))
                    print('\n')
        print("\n ---------------------------------------------------------------------\n")
        print('\n')
        print(bold + "Scatter plots : " + not_bold)
        print('\n')
        
        @widgets.interact(Select_x=df.columns.tolist(), Select_y=df.columns.tolist())
        def create_scatter(Select_x, Select_y):
            with plt.style.context("ggplot"):
                fig = plt.figure(figsize=(8,4))

                plt.scatter(x = df[Select_x],
                            y = df[Select_y],
                    #c=iris_df["FlowerType"],
                            s=20
                   )

                plt.xlabel(Select_x.capitalize())
                plt.ylabel(Select_y.capitalize())

                plt.title("%s vs %s"%(Select_x.capitalize(), Select_y.capitalize()))
                    
        print("\n ---------------------------------------------------------------------\n")
        print(bold + 'Correlation matrix :' + not_bold)
        print('\n')
        # correlation matrix and heatmap
        corr = df.corr()
        print(corr)
        print('\n')
        print('\n')
        print(bold + 'Heatmap :' + not_bold)
        print(sns.heatmap(corr, xticklabels=corr.columns, yticklabels=corr.columns , cmap="Blues"))
        
                    
        
        