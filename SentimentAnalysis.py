import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
import pandas as pd

class SentimentAnalyzer:
    def __init__(self):
        # Download required NLTK data
        nltk.download('vader_lexicon')
        nltk.download('punkt')
        self.sia = SentimentIntensityAnalyzer()
        
    def analyze_text(self, text):
        # VADER sentiment analysis
        vader_scores = self.sia.polarity_scores(text)
        
        # TextBlob analysis
        blob = TextBlob(text)
        
        return {
            'vader': vader_scores,
            'textblob': {
                'polarity': blob.sentiment.polarity,
                'subjectivity': blob.sentiment.subjectivity
            }
        }
    
    def analyze_file(self, filename):
        results = []
        
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                if line.strip():
                    analysis = self.analyze_text(line.strip())
                    results.append({
                        'text': line.strip(),
                        'vader_compound': analysis['vader']['compound'],
                        'textblob_polarity': analysis['textblob']['polarity']
                    })
        
        return pd.DataFrame(results)

def main():
    analyzer = SentimentAnalyzer()
    
    while True:
        print("\nSentiment Analysis Menu:")
        print("1. Analyze text input")
        print("2. Analyze text file")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ")
        
        if choice == '1':
            text = input("\nEnter text to analyze: ")
            results = analyzer.analyze_text(text)
            
            print("\nResults:")
            print("VADER Analysis:")
            print(f"Compound Score: {results['vader']['compound']}")
            print(f"Positive: {results['vader']['pos']}")
            print(f"Neutral: {results['vader']['neu']}")
            print(f"Negative: {results['vader']['neg']}")
            
            print("\nTextBlob Analysis:")
            print(f"Polarity: {results['textblob']['polarity']}")
            print(f"Subjectivity: {results['textblob']['subjectivity']}")
            
        elif choice == '2':
            filename = input("\nEnter filename to analyze: ")
            try:
                results_df = analyzer.analyze_file(filename)
                print("\nAnalysis Results:")
                print(results_df)
                
                # Save results to CSV
                output_file = f"sentiment_analysis_results_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv"
                results_df.to_csv(output_file, index=False)
                print(f"\nResults saved to {output_file}")
                
            except FileNotFoundError:
                print("File not found!")
                
        elif choice == '3':
            print("Thank you for using the Sentiment Analyzer!")
            break
            
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
