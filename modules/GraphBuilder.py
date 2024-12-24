import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from datetime import datetime
import matplotlib.dates as mdates
from datetime import timedelta

class GraphCreator:

    ###   ak sa nezmestia data tak dorobit legendu a do grafov priradit iba
    def __init__(self, data):
        self.table = None
        self.attendance_graph = None
        self.placement_graph = None
        self.times_graph = None
        self.data = data #[{month, year : participations}, {race : time_after_first}, {race : [date, placement]}, name, club, start_date, end_date]  +  mozno nejaku path z configuraku nwm
        
    def create_attendance_graph(self):
        fig1, ax1 = plt.subplots()
        mesiace = self.data[0].keys()
        participation = self.data[0].values()
        ax1.bar(mesiace, participation, color='hotpink')
        ax1.set_yticks(range(7))
        ax1.set_yticklabels(range(0,7))
        ax1.set_title("Účasť na pretekoch")
        return fig1

    def create_times_graph(self):
        time_differences = self.data[1].values()

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
        races = self.data[1].keys()
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

        
        
        race_data.sort(key=lambda x: x[1])
        
        race_names = self.data[2].keys()
        dates = [item[0] for item in self.data[2].values()]
        placements = [item[1] for item in self.data[2].values()]

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
            ["Meno", self.data[3]],
            ["Klub", self.data[4]],
            ["Časový interval", f"{self.data[5]} -> {self.data[6]}"]
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


i = GraphCreator([{month, year : participations}, {race : time_after_first}, {race : [date, placement]}, name, club, start_date, end_date])
#print(1)
i.create()
#print(2)
#i.save()
#print(3)

