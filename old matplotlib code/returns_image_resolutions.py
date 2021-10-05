import os
from re import L
from PIL import Image

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors

# currently used to return the mean value, may use for other statistics.



def calc_mean(list_of_values):
    # i'm sure there is code to do this for me.
    
    total = 0
    for i in list_of_values:
        try:
            total += i
        except:
            pass 

    return total / len(list_of_values)

def Open_and_get_res(filepath):
    try:
        im = Image.open(filepath)
        return im.size
    except:
        return (0,0)

def main(srcs, figtitle):
    x = np.empty(shape=(0))
    y = np.empty(shape=(0))

    i = 0
    for src_path in srcs:
        for root, dirs, files in os.walk(src_path):
            for f in files:
                i += 1
                
                filepath = os.path.join(root, f)
                size = Open_and_get_res(filepath)

                if size != (0,0):
                    x = np.append(x, size[0])
                    y = np.append(y, size[1])

                print("File: {} | [ {} x {} ]".format(i, size[0], size[1]))


    ## graph code

    #print(list(a for a in plt.rcParams if 'color' in a))
    
    with plt.rc_context({'axes.edgecolor':'white',
        'axes.titlecolor':'white',
        'axes.labelcolor':'white',
        'text.color':'white',
        'xtick.color':'white',
        'ytick.color':'white',
        'figure.facecolor':'black',
        }):
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
        fig.suptitle(figtitle) 
        fig.patch.set_facecolor('black')
        ax = ax1
        ax.set_title("Image Sizes")
        ax.margins(0)
        ax.set_xlabel("Width/pixels") 
        ax.set_ylabel("Height/pixels") 
        ax.set_facecolor('black')
        
        ax.grid(linewidth='0.3')
        ax.scatter(x, y, s=3.5, c='#e73f2f', alpha=0.1)
        ax.set_aspect("equal")
        ax.set_xticks(np.arange(0, max(x) + 1, 2000))
        ax.set_yticks(np.arange(0, max(y) + 1, 2000))

        n_bins = 250

        ax = ax2
        ax.margins(0)
        ax.set_title("Image Size Distribution (2d Histogram)")
        ax.set_facecolor('black')
        ax.set_xlabel("Width/pixels") 
        ax.set_ylabel("Height/pixels") 
        
        ax.hist2d(x, y, bins=100, norm=colors.LogNorm())
        ax.grid(linewidth='0.3')


        ax = ax3
        ax.margins(0)
        ax.set_title("Image Width Distribution")
        ax.set_facecolor('black')
        ax.set_xlabel("Width/pixels") 
        ax.set_ylabel("Frequency") 
        ax.grid(linewidth='0.3')
        ax.hist(x, bins=n_bins, color='#e73f2f')
        
        
        ax = ax4
        ax.margins(0)
        ax.set_title("Image Height Distribution")
        ax.set_facecolor('black')
        ax.set_xlabel("Height/pixels") 
        ax.set_ylabel("Frequency") 
        ax.grid(linewidth='0.3')
        ax.hist(y, bins=n_bins, color='#e73f2f')
        

    
    fig.show()

    print("\n")
    #print("Mean width: {} px".format(calc_mean(x)))
    #print("Mean height: {} px".format(calc_mean(y)))
    input()

if __name__ == "__main__":
    src_path = [r'']
    ic_path = [r'']
    main(src_path, "Image Sizes (MIR/ImR)")