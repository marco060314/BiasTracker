class CustomPipeline:
    def __init__(self):
        self.scraped_data = []

    def process_item(self, item, spider):
        self.scraped_data.append(item)
        return item