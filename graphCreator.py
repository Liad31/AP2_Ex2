import matplotlib.pyplot as plt
import mpld3

# import random
# numberOfLines = 50
# ys=[0]
# for i in range(1,numberOfLines):
#     ys.append(random.randint(ys[i-1]-10,ys[i-1]+10))
# spans = [[10, 230], [231,231]]

def plotGraph(ys, spans):
    fig = plt.figure(figsize=(7, 3.5))
    xs = []
    current = 0
    for i in range(len(ys)):
        xs.append(i)
    for span in spans:
        start = span[0]
        end = span[1]
        if current < start:
            plt.plot(xs[current : start + 1], ys[current : start + 1], color='b', linewidth=3)
        plt.plot(xs[start: end + 2], ys[start: end + 2], color='r', linewidth=3)
        current = end + 1
    plt.plot(xs[current : ], ys[current : ], color='b', linewidth=3)

    plt.grid(True, alpha=0.3)
    html_str = mpld3.fig_to_html(fig)
    Html_file = open("templates/graph.html", "w")
    Html_file.write(html_str)
    Html_file.close()
