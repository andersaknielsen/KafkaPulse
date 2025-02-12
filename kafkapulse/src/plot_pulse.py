import matplotlib.pyplot as plt

def plot_data(pulse_data) -> None:
    """
    Plots heart rate data over time.
    Parameters:
    pulse_data (list of tuples): A list where each tuple contains two elements:
                                 - The first element is the heart rate (int or float).
                                 - The second element is the datetime object representing the time of the heart rate measurement.
    Returns:
    None
    """
    if not pulse_data:
        raise ValueError("No data to plot")

    # x is datetime, y is heart rate
    x = [i[1] for i in pulse_data]
    y = [i[0] for i in pulse_data]
    # Plot over time. Handle the datetime objects
    fig, ax = plt.subplots()

    # # Format the x-axis
    # ax.xaxis.set_major_locator(mdates.SecondLocator(interval=10))
    # ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))

    ax.plot(x, y)
    ax.set(xlabel='Time', ylabel='Heart Rate',
            title='Heart Rate over Time')
    ax.grid()
    plt.show()