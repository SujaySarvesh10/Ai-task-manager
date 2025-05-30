from transformers import pipeline

class TaskClassifier:
    def __init__(self):
        self.categories = [
            "Health and Wellness",
            "Finance and Bills",
            "Study and Education",
            "Work and Office",
            "Shopping and Groceries",
            "Personal and Social",
            "Other"
        ]
        self.classifier = pipeline(
            "zero-shot-classification",
            model="facebook/bart-large-mnli"
        )

        # Custom keyword rules
        self.keyword_map = {
            "Health and Wellness": ["doctor", "dentist", "hospital", "clinic", "appointment", "checkup", "medicine"],
            "Finance and Bills": ["pay", "bill", "loan", "bank", "tax", "salary", "insurance"],
            "Shopping and Groceries": ["buy", "purchase", "groceries", "shopping", "store", "milk", "vegetables"],
            "Study and Education": ["study", "exam", "test", "assignment", "lecture", "class", "project"],
            "Work and Office": ["meeting", "email", "report", "work", "office", "deadline", "submit"],
        }

    def classify_task(self, task_text):
        # Rule-based boost
        lowered = task_text.lower()
        for category, keywords in self.keyword_map.items():
            if any(word in lowered for word in keywords):
                print(f"\n🧠 Rule matched for: {category}")
                return category

        # Fallback to model
        result = self.classifier(task_text, self.categories)
        print("\n🔍 Top Predictions:", result["labels"][:3])
        return result["labels"][0]
