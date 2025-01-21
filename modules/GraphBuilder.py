import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from datetime import datetime, timedelta

class GraphCreator:

    def __init__(self, data):
        self.table = None
        self.data = data
        self.figures = [] 

    def create_attendance_graph(self):
        participation_data = dict(self.data[0])
        
        start_date = self.data[5]
        end_date = self.data[6]

        
        current_date = start_date
        all_months = []
        while current_date <= end_date:
            
            all_months.append(f'{current_date.year}-{current_date.month}')
            current_date += timedelta(days=31) 
            current_date = current_date.replace(day=1)  
        
        participation_data = {month: participation_data.get(month, 0) for month in all_months}
        participation_items = list(participation_data.items())
        
        
        chunk_size = min([5, 6, 7], key=lambda size: (len(participation_items) % size != 0, -(len(participation_items) % size)))
        chunks = [participation_items[i:i + min(chunk_size, len(participation_items))] for i in range(0, len(participation_items), chunk_size)]
        max_value = max(participation_data.values())
        for idx, chunk in enumerate(chunks):
            fig, ax = plt.subplots()
            mesiace, participation = zip(*chunk)
            
            
            ax.bar(mesiace, participation, color='hotpink')
            
            
            ax.set_yticks(range(0, max_value + 2))
            ax.set_yticklabels(range(0, max_value + 2))
            
            ax.set_title(f"Účasť na pretekoch (Strana {idx + 1})")
            ax.set_xticks(range(len(mesiace)))
            ax.set_xticklabels(mesiace, rotation=30, ha="right", fontsize=8)
            
            plt.tight_layout() 
            self.figures.append(fig)

    def create_times_graph(self):
        races_times = list(self.data[1].items())
        chunk_size = min([6, 7, 8], key=lambda size: (len(races_times) % size != 0, -(len(races_times) % size)))
        chunks = [races_times[i:i + min(chunk_size, len(races_times))] for i in range(0, len(races_times), chunk_size)]
        
        for idx, chunk in enumerate(chunks):
            fig, ax = plt.subplots(figsize=(10, 6)) 
            races, time_differences = zip(*chunk)
            
            
            time_in_seconds = [
                sum(int(x) * 60 ** i for i, x in enumerate(str(td).split(":")[::-1])) for td in time_differences
            ]
            
            
            max_time = max(time_in_seconds)
            if max_time <= 1800:
                interval = 120  
            elif max_time <= 3600:
                interval = 300  
            elif max_time <= 7200:
                interval = 600
            else:
                interval = 900 
            
            yticks = range(0, max_time + interval, interval)
            formatted_yticks = [f"{t // 3600:02}:{(t // 60) % 60:02}:{t % 60:02}" for t in yticks]

            
            ax.plot(races, time_in_seconds, color='green', marker='o')
            ax.set_yticks(yticks)
            ax.set_yticklabels(formatted_yticks)
            ax.set_title(f"Časová strata oproti 1. miestu (Strana {idx + 1})")

            
            ax.set_xticks(range(len(races)))
            ax.set_xticklabels(races, rotation=30, ha="right", fontsize=8, wrap=True)

            plt.tight_layout()
            self.figures.append(fig)


    def create_placement_graph(self):
        placement_data = sorted(self.data[2].items(), key=lambda x: x[1][0])
        
        
        chunk_size = min([6, 7, 8], key=lambda size: (len(placement_data) % size != 0, -(len(placement_data) % size)))
        chunks = [placement_data[i:i + min(chunk_size, len(placement_data))] for i in range(0, len(placement_data), chunk_size)]
        
        for idx, chunk in enumerate(chunks):
            fig, ax = plt.subplots(figsize=(10, 6))

            
            race_names, data = zip(*chunk)
            dates, placements, total = zip(*data)

            result = []
            for i in range(len(placements)):
                if placements[i] in {1, 2, 3}:
                    result.append(placements[i])
                else:
                    if placements[i] == None:
                        placement = 0
                    else:
                        placement = int(placements[i])
                    ratio = placement / total[i]
                    if 0 < ratio <= 0.25:
                        result.append("1/4")
                    elif 0.25 < ratio <= 0.5:
                        result.append("1/2")
                    elif 0.5 < ratio <= 0.75:
                        result.append("3/4")
                    elif 0.75 < ratio <= 1.0:
                        result.append("4/4")

            
            mapping = {"4/4": 6, "3/4": 5, "1/2": 4, "1/4": 3, 3: 2, 2: 1, 1: 0}
            result_indices = [mapping[val] for val in result]

            
            y_labels = ["4/4", "3/4", "1/2", "1/4", 3, 2, 1][::-1]
            y_positions = list(range(len(y_labels)))

            ax.plot(range(len(result_indices)), result_indices, marker='o', color='blue', linestyle='-')
            ax.set_title(f"Umiestnenie v pretekoch (Strana {idx + 1})")
            ax.set_yticks(y_positions)
            ax.set_yticklabels(y_labels)
            ax.invert_yaxis()

            
            ax.set_xticks(range(len(dates)))
            ax.set_xticklabels(race_names, rotation=30, ha="right", fontsize=8, wrap=True)

            plt.tight_layout()
            self.figures.append(fig)



    def create_table(self):
        fig, ax = plt.subplots()
        ax.axis("tight")
        ax.axis("off")

        summary_data = [
            ["Meno", self.data[3]],
            ["Klub", self.data[4]],
            ["Časový interval", f"{self.data[5].year}.{self.data[5].month} -> {self.data[6].year}.{self.data[6].month}"]
        ]

        table = ax.table(cellText=summary_data, cellLoc="center", loc="center")
        table.scale(1, 2)
        table.auto_set_font_size(True)
        table.set_fontsize(12)

        self.figures.append(fig)

    def create(self):
        self.create_table()
        self.create_attendance_graph()
        self.create_times_graph()
        self.create_placement_graph()

    def save(self):
        with PdfPages("athlete_statistics.pdf") as pdf:
            for fig in self.figures:
                pdf.savefig(fig)
                plt.close(fig)


# Sample Data
data = [
    {  # Participation data
        "2020-01": 4, "2020-02": 3, "2020-03": 0, "2020-04": 3, "2020-05": 1,
        "2020-06": 0, "2020-07": 5, "2020-08": 4, "2020-09": 5, "2020-10": 1,
##        "2021-01": 4, "2021-02": 2, "2021-03": 0,
##        "2021-04": 3, "2021-05": 4, "2021-06": 5, "2021-07": 2, "2021-08": 5,
        "2021-09": 4, "2021-10": 5, "2022-11": 1, "2023-02": 3, "2023-03": 4,
        "2023-04": 1, "2023-05": 4, "2023-06": 3, "2023-07": 4, "2023-08": 0,
        "2023-09": 2, "2023-10": 3, "2023-11": 3, "2023-12": 2
    },
    {  # Time differences data
##        "Pretek kyselinarov v hontianskych nemcoch": "04:18:11", "Cezpolny beh olazskych zvaracov": "00:08:43", "Stofersky maraton po sites of lucanka": "00:30:25",
##        "Race_4": "02:34:55", "Race_5": "04:22:33", "Race_6": "04:22:01",
##        "Race_7": "03:13:46", "Race_8": "01:36:02", "Race_9": "02:15:06",
##        "Race_10": "03:52:10"
        "Pretek kyselinarov v hontianskych nemcoch": "00:18:11", "Cezpolny beh olazskych zvaracov": "00:08:43", "Stofersky maraton po sites of lucanka": "00:30:25",
        "Race_4": "00:20:55", "Race_5": "00:22:33", "Race_6": "00:15:01",
        "Race_7": "00:13:46", "Race_8": "00:22:02", "Race_9": "00:04:06",
        "Race_10": "00:00:00"
    },
    {  # Placement data
        "Pretek kyselinarov v hontianskych nemcoch": ["2023-07-15", 36, 90],
        "Sprint o zrdi na 325 metrov": ["2020-03-16", 77, 200],
        "Race_3": ["2022-12-05", 58, 100], "Race_4": ["2022-05-22", 96, 100],
        "Race_5": ["2020-04-22", 48, 50], "Race_6": ["2023-02-26", 15, 1000],
        "Race_7": ["2022-07-01", 51, 68], "Race_8": ["2020-07-21", 25, 25],
        "Race_9": ["2022-12-07", 3, 35], "Race_10": ["2022-10-27", 1, 4]
    },
    "John Doe",
    "Speedsters Club",
    "2020-01-01 00:00:00",
    "2023-12-31 00:00:00"
]

# Usage
# i = GraphCreator(data)
# i.create()
# i.save()

