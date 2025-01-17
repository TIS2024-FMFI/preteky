import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from datetime import datetime

class GraphCreator:

    def __init__(self, data):
        self.table = None
        self.data = data
        self.figures = []  # Store all figures for saving later

    def create_attendance_graph(self):
        participation_data = list(self.data[0].items())
        chunks = [participation_data[i:i + 7] for i in range(0, len(participation_data), 7)]
        for idx, chunk in enumerate(chunks):
            fig, ax = plt.subplots()
            mesiace, participation = zip(*chunk)
            ax.bar(mesiace, participation, color='hotpink')
            ax.set_yticks(range(7))
            ax.set_yticklabels(range(0, 7))
            ax.set_title(f"Účasť na pretekoch (Strana {idx + 1})")
            self.figures.append(fig)

    def create_times_graph(self):
        races_times = list(self.data[1].items())
        chunks = [races_times[i:i + 7] for i in range(0, len(races_times), 7)]
        for idx, chunk in enumerate(chunks):
            fig, ax = plt.subplots(figsize=(10, 6))  # Adjust figure size for better readability
            races, time_differences = zip(*chunk)
            time_in_seconds = [
                sum(int(x) * 60 ** i for i, x in enumerate(td.split(":")[::-1])) for td in time_differences
            ]
            yticks = range(0, max(time_in_seconds) + 600, 600)
            formatted_yticks = [f"{t // 3600:02}:{(t // 60) % 60:02}:{t % 60:02}" for t in yticks]

            ax.plot(races, time_in_seconds, color='green', marker='o')
            ax.set_yticks(yticks)
            ax.set_yticklabels(formatted_yticks)
            ax.set_title(f"Časová strata oproti 1. miestu (Strana {idx + 1})")
            #ax.set_xlabel("Race")
            #ax.set_ylabel("Časová strata (HH:MM:SS)")

            # Adjust x-axis labels for longer names
            ax.set_xticks(range(len(races)))
            ax.set_xticklabels(races, rotation=30, ha="right", fontsize=8, wrap=True)

            plt.tight_layout()  # Automatically adjust layout to fit elements
            self.figures.append(fig)

    def create_placement_graph(self):
        # Sort all placement data by date before chunking
        placement_data = sorted(self.data[2].items(), key=lambda x: datetime.strptime(x[1][0], "%Y-%m-%d"))
        
        # Divide sorted data into chunks
        chunks = [placement_data[i:i + 7] for i in range(0, len(placement_data), 7)]
        
        for idx, chunk in enumerate(chunks):
            fig, ax = plt.subplots(figsize=(10, 6))

            # Extract race names and data from chunk
            race_names, data = zip(*chunk)
            dates, placements, total = zip(*data)

            # Calculate result
            result = []
            for i in range(len(placements)):
                if placements[i] in {1, 2, 3}:
                    result.append(placements[i])
                else:
                    ratio = placements[i] / total[i]
                    if 0 < ratio <= 0.25:
                        result.append("1/4")
                    elif 0.25 < ratio <= 0.5:
                        result.append("1/2")
                    elif 0.5 < ratio <= 0.75:
                        result.append("3/4")
                    elif 0.75 < ratio <= 1.0:
                        result.append("4/4")

            # Map result to indices for plotting
            mapping = {"4/4": 6, "3/4": 5, "1/2": 4, "1/4": 3, 3: 2, 2: 1, 1: 0}
            result_indices = [mapping[val] for val in result]

            # Plot
            y_labels = ["4/4", "3/4", "1/2", "1/4", 3, 2, 1][::-1]
            y_positions = list(range(len(y_labels)))

            ax.plot(range(len(result_indices)), result_indices, marker='o', color='blue', linestyle='-')
            ax.set_title(f"Umiestnenie v pretekoch (Strana {idx + 1})")
            ax.set_yticks(y_positions)
            ax.set_yticklabels(y_labels)
            ax.invert_yaxis()

            # Adjust x-axis labels
            ax.set_xticks(range(len(dates)))
            ax.set_xticklabels(race_names, rotation=30, ha="right", fontsize=8)

            plt.tight_layout()  # Automatically adjust layout to fit elements
            self.figures.append(fig)



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
        "2021-01": 4, "2021-02": 2, "2021-03": 0,
        "2021-04": 3, "2021-05": 4, "2021-06": 5, "2021-07": 2, "2021-08": 5,
        "2021-09": 4, "2021-10": 5, "2022-11": 1, "2023-02": 3, "2023-03": 4,
        "2023-04": 1, "2023-05": 4, "2023-06": 3, "2023-07": 4, "2023-08": 0,
        "2023-09": 2, "2023-10": 3, "2023-11": 3, "2023-12": 2
    },
    {  # Time differences data
        "Pretek kyselinarov v hontianskych nemcoch": "04:18:11", "Cezpolny beh olazskych zvaracov": "00:08:43", "Stofersky maraton po sites of lucanka": "00:30:25",
        "Race_4": "02:34:55", "Race_5": "04:22:33", "Race_6": "04:22:01",
        "Race_7": "03:13:46", "Race_8": "01:36:02", "Race_9": "02:15:06",
        "Race_10": "03:52:10"
    },
    {  # Placement data
        "Pretek kyselinarov v hontianskych nemcoch": ["2023-07-15", 36, 90],
        "Race_2": ["2020-03-16", 77, 200],
        "Race_3": ["2022-12-05", 58, 100], "Race_4": ["2022-05-22", 96, 100],
        "Race_5": ["2020-04-22", 48, 50], "Race_6": ["2023-02-26", 15, 1000],
        "Race_7": ["2022-07-01", 51, 68], "Race_8": ["2020-07-21", 25, 25],
        "Race_9": ["2022-12-07", 3, 35], "Race_10": ["2022-10-27", 1, 4]
    },
    "John Doe",
    "Speedsters Club",
    "2020-01-01",
    "2023-12-31"
]

# Usage
i = GraphCreator(data)
i.create()
i.save()
