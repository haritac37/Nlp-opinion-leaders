# Nlp-opinion-leaders
Opinion Leader Identification using NLP
## MBA Business Analytics — NLP Project | Woxsen University 2027

### Problem Statement
Identify opinion leaders among Amazon Fine Food reviewers whose reviews
disproportionately influence other customers' purchasing decisions,
using NLP-based authority scoring and sentiment analysis.

### Dataset
Amazon Fine Food Reviews — 568K reviews from Kaggle
https://www.kaggle.com/datasets/snap/amazon-fine-food-reviews

### How to Run
1. Open `Opinion_Leader_NLP.ipynb` in Google Colab
2. Upload `Reviews.csv` to the Colab file panel
3. Run all cells in order (Runtime → Run All)

### Project Structure
- `Opinion_Leader_NLP.ipynb` — Main notebook (all steps)
- `plots/` — All output visualizations
- `README.md` — This file

### Methodology
- Text preprocessing: tokenization, lemmatization, stopword removal
- Feature engineering: helpfulness ratio, sentiment polarity, review breadth
- Scoring model: weighted composite Opinion Leader Score (MinMax scaled)
- Visualizations: bar charts, scatter plots, heatmaps, word cloud

### Tools & Libraries
Python · NLTK · TextBlob · Scikit-learn · Pandas · Matplotlib · Seaborn · WordCloud
"""
