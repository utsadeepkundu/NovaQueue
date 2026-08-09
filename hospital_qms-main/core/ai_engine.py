from textblob import TextBlob

class MedicalAIEngine:
    @staticmethod
    def analyze_urgency(symptoms):
        """
        Analyzes symptoms and returns an urgency score from 1.0 to 10.0.
        Includes 'Code Red' logic for emergency detection.
        """
        symptoms_lower = symptoms.lower()
        
        # 1. CODE RED: Critical Emergency Keywords
        # These bypass standard sentiment and immediately set max priority
        critical_keywords = [
            'heart attack', 'chest pain', 'unconscious', 'cannot breathe', 
            'severe bleeding', 'seizure', 'heavy bleeding', 'choking',
            'poisoning', 'stroke', 'paralysis', 'breathing difficulty'
        ]
        
        for keyword in critical_keywords:
            if keyword in symptoms_lower:
                return 10.0  # Maximum Priority (Code Red)

        # 2. Standard AI Analysis (Sentiment-based)
        analysis = TextBlob(symptoms)
        
        # Scale: Polarity is -1 (Negative/Pain) to 1 (Positive)
        # We want Negative polarity to equal Higher Urgency
        # Score = (1 - polarity) * 5 (gives 0 to 10 range)
        base_score = (1 - analysis.sentiment.polarity) * 5
        
        # Add weights for semi-critical terms
        semi_critical = ['severe', 'acute', 'intense', 'vomiting', 'fever', 'fracture']
        for word in semi_critical:
            if word in symptoms_lower:
                base_score += 1.5
        
        # Clamp between 1.0 and 9.5 (Reserved 10.0 for Code Red)
        return min(max(base_score, 1.0), 9.5)

    @staticmethod
    def predict_wait_time(waiting_count, urgency_score):
        """
        Predicts wait time in minutes.
        Higher urgency = Lower wait time.
        """
        # Base time per patient is 15 mins
        # If score is 10.0 (Code Red), time is effectively 0
        if urgency_score >= 10.0:
            return 0
            
        base_time = waiting_count * 15
        reduction_factor = urgency_score / 10.0
        
        # The higher the urgency, the more we 'skip' the base time
        estimated = base_time * (1 - (reduction_factor * 0.5))
        return int(max(estimated, 5))