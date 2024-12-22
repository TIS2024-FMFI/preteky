import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from datetime import datetime
import matplotlib.dates as mdates
from datetime import timedelta

class GraphCreator:

    ###   dorobit input dat a nech sa zmestia nazvy
    def __init__(self):
        self.table = None
        self.attendance_graph = None
        self.placement_graph = None
        self.times_graph = None
        
    def create_attendance_graph(self):
        fig1, ax1 = plt.subplots()
        mesiace = ["Január", "Február", "Marec", "April", "Máj", "Jún"]
        participation = [1, 0, 3, 1, 2, 2]
        ax1.bar(mesiace, participation, color='hotpink')
        ax1.set_yticks(range(7))
        ax1.set_yticklabels(range(0,7))
        ax1.set_title("Účasť na pretekoch")
        return fig1

    def create_times_graph(self):
        time_differences = [
            timedelta(minutes=4),
            timedelta(minutes=10, seconds=23),
            timedelta(minutes=1, seconds=45),
            timedelta(hours=1, minutes=5, seconds=30)  # Example with hours
        ]

        time_in_seconds = [td.total_seconds() for td in time_differences]

        min_seconds = int(min(time_in_seconds))
        max_seconds = int(max(time_in_seconds))

        time_range = max_seconds - min_seconds
        if time_range <= 3600:
            interval = 60
        elif time_range <= 7200:
            interval = 300 
        else:
            interval = 600

        yticks = range(0, max_seconds + interval, interval)

        formatted_yticks = [f"{t // 3600:02}:{(t // 60) % 60:02}:{t % 60:02}" for t in yticks]

        fig2, ax2 = plt.subplots()
        races = ["Race 1", "Race 2", "Race 3", "Race 4"]
        ax2.plot(races, time_in_seconds, color='green', marker='o', label="Time loss (seconds)")


        for y in time_in_seconds:
            ax2.hlines(y, xmin=-0.5, xmax=len(races) - 1 + 0.5, colors='gray', linestyles='dashed', alpha=0.5)

        ax2.set_yticks(yticks)
        ax2.set_yticklabels(formatted_yticks)

        ax2.set_title("Časová strata oproti 1. miestu")
        ax2.set_xlabel("Race")
        ax2.set_ylabel("Časová strata (HH:MM:SS)")
        return fig2


    def create_placement_graph(self):
        fig, ax = plt.subplots()

        race_data = [
            ("Race A\n\n\n\n", datetime(2023, 1, 10), 3),
            ("Race B", datetime(2023, 3, 5), 1),
            ("Race C", datetime(2023, 6, 20), 5),
            ("Race D", datetime(2023, 9, 15), 4)
        ]
        
        race_data.sort(key=lambda x: x[1])
        
        race_names = [item[0] for item in race_data]
        dates = [item[1] for item in race_data]
        placements = [item[2] for item in race_data]

        y_labels = ["4/4","3/4", "1/2", "1/4", 3, 2, 1][::-1]
        y_positions = list(range(len(y_labels)))
        
        ax.plot(dates, placements, marker='o', color='blue', linestyle='-')
        ax.set_title("Umiestnenie v pretekoch")

        ax.set_yticks(y_positions)
        ax.set_yticklabels(y_labels)
        ax.invert_yaxis()

        ax.set_xticks(dates)
        print(race_names)
        ax.set_xticklabels(race_names, rotation=0)

        return fig



    def create_table(self):
        fig, ax = plt.subplots()
        ax.axis("tight")
        ax.axis("off")

        summary_data = [
            ["Meno", "Alexander Fekete"],
            ["Klub", "Pretekársky klub Rimavská sobota"],
            ["Časový interval", "1.1.2000 -> 2.2.2002"]
        ]

        table = ax.table(cellText=summary_data, cellLoc="center", loc="center")
        table.scale(1, 2) 
        table.auto_set_font_size(True)
        table.set_fontsize(12)

        return fig

    def create(self):
        self.table = self.create_table()
        self.placement_graph = self.create_placement_graph()
        self.times_graph = self.create_times_graph()
        self.attendance_graph = self.create_attendance_graph()
    
    def save(self):
        with PdfPages("athlete_statistics.pdf") as pdf:
            for fig in [self.table, self.placement_graph, self.times_graph, self.attendance_graph]:
                pdf.savefig(fig) 
                plt.close(fig)


#i = GraphCreator()
#print(1)
#i.create()
#print(2)
#i.save()
#print(3)
