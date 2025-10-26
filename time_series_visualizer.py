import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#charge the dataset and clean it
df = pd.read_csv("fcc-forum-pageviews.csv", parse_dates=['date'], index_col='date') #load the data into a DataFrame parsing the date column as datetime and setting it as index
df = df[(df["value"] >= df["value"].quantile(0.025)) & (df["value"] <= df["value"].quantile(0.975))] #remove the top and bottom 2.5% of the data to eliminate outliers

#line plot function 
def draw_line_plot(): #create a line plot showing the daily page views over time
    df_line = df.copy() #create a copy of the cleaned DataFrame
    fig, ax = plt.subplots(figsize=(15,5)) #set the figure size
    ax.plot(df_line.index, df_line["value"], color="red") #plot the line graph
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019") #set the title
    ax.set_xlabel("Date") #set the x-axis label
    ax.set_ylabel("Page Views") #set the y-axis label
    fig.savefig("line_plot.png") #save the figure
    return fig

#bar plot function
def draw_bar_plot(): #create a bar plot showing average monthly page views for each year
    df_bar = df.copy() #create a copy of the cleaned DataFrame
    df_bar['year'] = df_bar.index.year #extract year from the index
    df_bar['month'] = df_bar.index.month_name() #extract month name from the index
    months_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'] #define the order of months
    grouped = (  #group the data by year and month and calculate the mean page views per month
        df_bar.groupby(['year', 'month'])['value']
        .mean()
        .reset_index() #reset the index to turn the groupby object back into a DataFrame
    )
    fig, ax = plt.subplots(figsize=(12,8)) #set the figure size
    sns.barplot(data=grouped, x="year", y="value", hue="month", ax=ax)
    ax.set_xlabel("Years") #set the x-axis label
    ax.set_ylabel("Average Page Views") #set the y-axis label
    ax.legend(title="Months")
    fig.savefig("bar_plot.png") #save the figure
    return fig

def draw_box_plot(): #create box plots to show distributions of page views by year and by month
    df_box = df.copy().reset_index() #create a copy of the cleaned DataFrame and reset the index
    df_box['year'] = df_box['date'].dt.year #extract year from the date column
    df_box['month'] = df_box['date'].dt.strftime('%b') #extract month abbreviation from the date column
    months_order = ['Jan', 'Feb', ' Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'] #define the order of months
    df_box['month'] = pd.Categorical(df_box['month'], categories=months_order, ordered=True) #set the month column as a categorical variable with the defined order
    fig, axes = plt.subplots(1, 2, figsize=(15,6)) #set the figure size and create subplots
    # Year-wise box plot
    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0]) 
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')
    # Month-wise box plot
    sns.boxplot(x='month', y='value', data=df_box, ax=axes[1])
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')
    fig.savefig("box_plot.png") #save the figure
    return fig
if __name__ == "__main__":
    draw_line_plot()
    draw_bar_plot()
    draw_box_plot()