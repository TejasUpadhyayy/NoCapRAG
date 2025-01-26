from collections import defaultdict
import datetime

class TrendPredictor:
    def __init__(self):
        self.trend_data = defaultdict(list)  # Stores meme mentions over time

    def add_data(self, meme, timestamp=None):
        """Add meme mention data."""
        if not timestamp:
            timestamp = datetime.datetime.now()
        self.trend_data[meme].append(timestamp)

    def predict_trends(self):
        """Predict emerging trends based on recent activity."""
        trends = []
        for meme, timestamps in self.trend_data.items():
            if len(timestamps) > 5:  # At least 5 mentions to consider
                recent_mentions = [ts for ts in timestamps if (datetime.datetime.now() - ts).days < 7]
                if len(recent_mentions) > 3:  # Trending if mentioned 3+ times in the last week
                    trends.append(meme)
        return trends