import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from PIL import Image
import random
import seaborn as sns
import numpy as np
colors =["#1D2026","#393939","#666666","#BDBDBD","#E0E0E0","#F2F2F2","#FD93B1","#FC2964","#FEC9D8","#FD5F8B","#0095FF","#E6F5FF","#5C33F6","#8566F8",]

def bar_chart_new():
    fig, ax = plt.subplots()

    fruits = ['apple', 'blueberry', 'cherry', 'orange']
    counts = [40, 100, 30, 55]
    bar_labels = ['red', 'blue', '_red', 'orange']
    bar_colors = ['tab:red', 'tab:blue', 'tab:red', 'tab:orange']

    ax.bar(fruits, counts, label=bar_labels, color=bar_colors)

    ax.set_ylabel('fruit supply')
    ax.set_title('Fruit supply by kind and color')
    ax.legend(title='Fruit color')
    name = random.random()
    plt.savefig(str(name) + '.png')
    im = Image.open(str(name) + '.png') 
    im.show() 
    # plt.show()

def bar_chart( categories, series, **optional_params):
    fig, ax = plt.subplots()
    bar_labels =[]
    if('bar_labels' in optional_params):
        bar_labels = optional_params['bar_labels']
    else:
        for i in range(0, len(categories)+ 1,1):
            bar_labels.append(i)

    bar_colors =[]
    if('bar_labels' in optional_params):
        bar_colors = optional_params['bar_labels']
    else:
        for i in range(0, len(categories)+ 1,1):
            bar_colors.append(colors[i])
 
    ax.bar(categories, series,label=bar_labels ,color=bar_colors)
    if ('ylabel' in optional_params):
        ax.set_ylabel(optional_params['ylabel'])
    if ('title' in optional_params):
        ax.set_title(optional_params['title'])
    if ('legend' in optional_params):
        ax.legend(title=optional_params['legend'])
    name = random.random()
    plt.savefig(str(name) + '.png')
    im = Image.open(str(name) + '.png') 
    im.show() 
  

def column_chart( categories, series, **optional_params):
    fig, ax = plt.subplots()
    bar_labels =[]
    if('bar_labels' in optional_params):
        bar_labels = optional_params['bar_labels']
    else:
        for i in range(0, len(categories)+ 1,1):
            bar_labels.append(i)

    bar_colors =[]
    if('bar_labels' in optional_params):
        bar_colors = optional_params['bar_labels']
    else:
        for i in range(0, len(categories)+ 1,1):
            bar_colors.append(colors[i])
 
    ax.barh(categories, series,label=bar_labels ,color=bar_colors)
    if ('ylabel' in optional_params):
        ax.set_ylabel(optional_params['ylabel'])
    if ('title' in optional_params):
        ax.set_title(optional_params['title'])
    if ('legend' in optional_params):
        ax.legend(title=optional_params['legend'])
    name = random.random()
    plt.savefig(str(name) + '.png')
    im = Image.open(str(name) + '.png') 
    im.show() 
  
  

def stack_bar( categories, below,above, **optional_params):
    species = categories
    weight_counts = {
        "Below": np.array(below),
        "Above": np.array(above),
    }
    width = 0.5
    fig, ax = plt.subplots()
    bottom = np.zeros(3)
    for boolean, weight_count in weight_counts.items():
        p = ax.bar(species, weight_count, width, label=boolean, bottom=bottom)
        bottom += weight_count
    if ('ylabel' in optional_params):
        ax.set_ylabel(optional_params['ylabel'])
    if ('title' in optional_params):
        ax.set_title(optional_params['title'])
    if ('legend' in optional_params):
        ax.legend(title=optional_params['legend'])
    name = random.random()
    plt.savefig(str(name) + '.png')
    im = Image.open(str(name) + '.png') 
    im.show() 
  

def line_graph( categories, series, **optional_params):
    # Plot the data
    fig, ax = plt.subplots()
    ax.plot(categories, series,color= colors[0])
    if ('ylabel' in optional_params):
        ax.set_ylabel(optional_params['ylabel'])
    if ('title' in optional_params):
        ax.set_title(optional_params['title'])
    if ('legend' in optional_params):
        ax.legend(title=optional_params['legend'])
    name = random.random()
    plt.savefig(str(name) + '.png')
    im = Image.open(str(name) + '.png') 
    im.show() 
  
def heat_graph( data,  **optional_params):
    fig, ax = plt.subplots()
    data= np.array(data)
    color =colors[0]
    cmap = mcolors.LinearSegmentedColormap.from_list('my_colormap', [color, color])
    sns.heatmap(data, annot=True, cmap=cmap, alpha=data)
    if ('ylabel' in optional_params):
        ax.set_ylabel(optional_params['ylabel'])
    if ('title' in optional_params):
        ax.set_title(optional_params['title'])
    if ('legend' in optional_params):
        ax.legend(title=optional_params['legend'])
    name = random.random()
    plt.savefig(str(name) + '.png')
    im = Image.open(str(name) + '.png') 
    im.show()                  
    
def histogram_graph(data , bins ,**optional_params):
    fig, ax = plt.subplots()
    plt.hist(data, bins, edgecolor='black',color=colors[0])
    if ('ylabel' in optional_params):
        ax.set_ylabel(optional_params['ylabel'])
    if ('title' in optional_params):
        ax.set_title(optional_params['title'])
    if ('legend' in optional_params):
        ax.legend(title=optional_params['legend'])
    name = random.random()
    plt.savefig(str(name) + '.png')
    im = Image.open(str(name) + '.png') 
    im.show()        
  
def waterfall_graph(categories,values ,   **optional_params):
    fig, ax = plt.subplots()
    cumulative_values = [sum(values[:i+1]) for i in range(len(values))]
    plt.bar(categories, values, color=colors[0], align='center', width=0.5)
    plt.plot(categories, cumulative_values, marker='o', color=colors[1], linestyle='--')
    if ('ylabel' in optional_params):
        ax.set_ylabel(optional_params['ylabel'])
    if ('title' in optional_params):
        ax.set_title(optional_params['title'])
    if ('legend' in optional_params):
        ax.legend(title=optional_params['legend'])
    name = random.random()
    plt.savefig(str(name) + '.png')
    im = Image.open(str(name) + '.png') 
    im.show()        

  
def dot_graph(categories, data,**optional_params):
    fig, ax = plt.subplots()
    plt.scatter(categories,data,color=colors[0])
    if ('ylabel' in optional_params):
        ax.set_ylabel(optional_params['ylabel'])
    if ('title' in optional_params):
        ax.set_title(optional_params['title'])
    if ('legend' in optional_params):
        ax.legend(title=optional_params['legend'])
    name = random.random()
    plt.savefig(str(name) + '.png')
    im = Image.open(str(name) + '.png') 
    im.show()        


# categories =['test- A','B','C','D','E'] # x axis category
# series = [{"name":"Name 1","data" :  [14,14   ,14]},   {"name":"Name 2","data" :   [7,5   ,3]   }] # Series to display multiple

# res = stack_bar(categories,series)
# print(res)

# data = [ {"name" : "hours-per-week" , "data" :  [11,12,13,14,15,6] },{"name" : "age" , "data" :[1,2,3,4,5,6]},{"name" : "age" , "data" :[3,4,5,6,7,8]}]

# res =forest_graph( "test", data)
# print(res )
# data = [{      "name": 'Line Data',     "data": [10, 20, 15, 25, 18],      "color": 'red',}]
# test = [{        "name": 'Line Data',     "data": [10, 20, 15, 25, 18],      "color": 'red',}]

# res =spline_graph( ['Jan', 'Feb', 'Mar', 'Apr', 'May'] , data, test)
# print(res )
