"""
Ghostbusters line plotting for HW3, copied out of HW3.py.

plot_lines() takes a list of lines, where each line is a pair of [x, y] points, and draws
them with matplotlib in a new window. Passing None plots a built-in set of three sample lines.
The window closes itself after display_seconds (10 by default). Passing show=False only draws
the window, so several can be drawn and then kept open together with one plt.show() call.
"""
import matplotlib.pyplot as plt


def plot_lines(lines, display_seconds=10, title=None, show=True):
    # display_seconds: how long the plot window stays open before closing itself.
    # Pass None to keep the window open until it is closed by hand.
    # title: optional text shown above the plot.
    # show: when False the window is drawn but not shown, and display_seconds is ignored.
    if lines == None:
        lines = []
        line1 = []
        line1.append([34,-205])
        line1.append([12,-117])
        lines.append(line1)

        line2 = []
        line2.append([38, 1009])
        line2.append([9, 226])
        lines.append(line2)

        line3 = []
        line3.append([11, 226])
        line3.append([17, 386])
        lines.append(line3)


    plt.figure()
    for line_number in range(len(lines)):
        line = lines[line_number]
        point1 = line[0]
        point2 = line[1]
        x_vals = []
        x_vals.append(point1[0])
        x_vals.append(point2[0])
        y_vals = []
        y_vals.append(point1[1])
        y_vals.append(point2[1])

        line_label = "line " + str(line_number)
        plt.plot(x_vals, y_vals, label = line_label)

    plt.legend()
    if title != None:
        plt.title(title)
    if not show:
        return
    if display_seconds == None:
        plt.show()
    else:
        plt.show(block=False)
        plt.pause(display_seconds)
        plt.close()


if __name__ == "__main__":
    plot_lines(None)
