from DateConverter import DateConverter


class CompetitionFormatter:
    def __init__(self, competition_data):
        self.data = competition_data
        self.required_keys = ['id', 'title_sk', 'date_from', 'date_to', 'categories']
        self.validate_data()
        self.date_converter = DateConverter()

    def validate_data(self):
        for key in self.required_keys:
            if key not in self.data:
                raise ValueError(f"Missing required key: {key}")
            if not isinstance(self.data[key], str) and key != 'categories':
                raise ValueError(f"Invalid data type for key: {key}")
        if not isinstance(self.data['categories'], list):
            raise ValueError("Invalid data type for key: categories")

    def get_competition_info(self):
        datum = self.date_converter.date_converter(self.data['date_from'])
        deadline = self.date_converter.date_converter(self.data['deadline'])
        return {
            "id": self.data['id'],
            "nazov": self.data['title_sk'],
            "datum": datum,
            "deadline": deadline,
            "poznamka": self.data.get('organizer_txt', '')
        }

    def get_categories(self):
        categories = []
        for category in self.data['categories']:
            categories.append({
                "id": category['id'],
                "category_id": category['category_id'],
                "name": category['category_name']
            })
        return categories

    def format(self):
        return {
            "competition": self.get_competition_info(),
            "categories": self.get_categories()
        }
