import io
import base64
import numpy as np
from urllib.parse import quote
import matplotlib.pyplot as plt

plt.switch_backend('Agg')

def pie_chart(scores):

    if not scores:
        return None, False
        
    plt.style.use('ggplot')
    plt.rc("font", family="serif")

    labels = ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'F']
    bins = [0]*11

    for score in scores:
        try:
            score = score[0]/score[1]
            if score >= .93: #A
                bins[0]+=1
            elif score >= .90: #A-
                bins[1]+=1
            elif score >= .87: #B+
                bins[2]+=1
            elif score >= .83: #B
                bins[3]+=1
            elif score >= .77: #B-
                bins[4]+=1
            elif score >= .73: #C+
                bins[5]+=1
            elif score >= .70: #C
                bins[6]+=1
            elif score >= .67: #C-
                bins[7]+=1
            elif score >= .63: #D+
                bins[8]+=1
            elif score >= .60: #D
                bins[9]+=1
            else: #F
                bins[10]+=1
        except:
            pass

    for i in range(len(labels)):
        if not bins[i]:
            labels[i] = ''
    success = bins != [0]*11
    plt.gca().set_prop_cycle('color', [plt.cm.Greens(i) for i in np.linspace(0.5,0.95,11)][::-1])
    plt.pie(bins, labels=labels, textprops={'fontsize': 18})
    plt.gca().axis('equal')
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    plt.close()
    img.seek(0)
    pie_chart = quote(base64.b64encode(img.read()).decode())
    return pie_chart, success

def cum_pct(scores):

    if not scores:
        return None, False

    plt.style.use('ggplot')
    plt.rc("font", family="serif")

    total_num = 0
    total_denom = 0
    cumulative = []
    for score in scores:
        num, denom = score
        total_num += num
        total_denom += denom
        try:
            cumulative.append(round(100 * total_num/total_denom, 2))
        except:
            pass
    success = len(cumulative) >= 2
    plt.plot(cumulative, color=plt.cm.Greens(0.95))
    plt.xticks([])
    plt.xlabel('*weighted by number of points')
    plt.title('Course Grade* (%) Over Time')
    plt.text(0.96, 0.96, str(cumulative[-1])+'%', fontsize=24, transform=plt.gca().transAxes, ha='right', va='top')
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    plt.close()
    img.seek(0)
    plot = quote(base64.b64encode(img.read()).decode())
    return plot, success