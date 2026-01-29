from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.services.text_preprocessor import TextPreprocessor
import numpy as np

class TfidfService:
    def __init__(self):
        self.preprocessor = TextPreprocessor()

    # -------------------------
    # SIMILARITY CALCULATION
    # -------------------------
    def calculate_similarity(self, text1, text2):
        """
        Calculate cosine similarity between resume and job description
        """
        processed_texts = [
            self.preprocessor.preprocess(text1),
            self.preprocessor.preprocess(text2)
        ]

        vectorizer = TfidfVectorizer(
            max_features=1500,
            ngram_range=(1, 2),
            stop_words="english"
        )

        try:
            tfidf_matrix = vectorizer.fit_transform(processed_texts)

            similarity = cosine_similarity(
                tfidf_matrix[0:1],
                tfidf_matrix[1:2]
            )[0][0]

            return float(similarity)

        except Exception as e:
            print(f"Error calculating similarity: {e}")
            return 0.0

    # -------------------------
    # ATS SCORE
    # -------------------------
    def calculate_ats_score(self, resume_text, job_description):
        similarity = self.calculate_similarity(resume_text, job_description)
        return round(similarity * 100, 2)

    # -------------------------
    # KEYWORD EXTRACTION
    # -------------------------
    def get_top_keywords(self, text, top_n=10):
        """
        Extract keywords from a SINGLE document using TF-IDF
        """
        processed_text = self.preprocessor.preprocess(text)

        vectorizer = TfidfVectorizer(
            max_features=top_n * 5,
            ngram_range=(1, 2),
            stop_words="english",
            max_df=1.0,   # IMPORTANT for single document
            min_df=1
        )

        try:
            tfidf_matrix = vectorizer.fit_transform([processed_text])
            feature_names = vectorizer.get_feature_names_out()
            scores = tfidf_matrix.toarray()[0]

            keyword_scores = list(zip(feature_names, scores))
            keyword_scores.sort(key=lambda x: x[1], reverse=True)

            return [(k, round(v, 4)) for k, v in keyword_scores if v > 0][:top_n]

        except Exception as e:
            print(f"Error extracting keywords: {e}")
            return []
