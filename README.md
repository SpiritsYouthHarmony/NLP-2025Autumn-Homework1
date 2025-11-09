
# Homework 1 - UCAS NLP

This repository contains the implementation and solutions for Homework 1 of the UCAS Natural Language Processing course. The project focuses on analyzing Chinese and English text corpora to study natural language patterns, including Zipf's Law validation, entropy calculations, and frequency analysis.

## Project Structure

```
.
├── cal_ch.py              # Chinese character entropy calculation
├── cal_en_letters.py      # English letter entropy calculation
├── cal_en_words.py        # English word entropy calculation
├── cal_scale.py           # Text corpus scale statistics
├── ch_crawl.py            # Chinese web crawler (Xinhua News)
├── ch_top10.py            # Top 10 Chinese characters frequency analysis
├── en_crawl.py            # English web crawler (Xinhua News & People's Daily)
├── en_top10.py            # Top 10 English words frequency analysis
├── zipf.py                # Zipf's Law validation
├── english.news/          # English news corpus
├── en.people/             # People's Daily English corpus
├── xinhuawang/            # Xinhua News Chinese corpus
├── renminwang/            # People's Daily Chinese corpus
└── images/                # Output charts and figures
```

## Key Features

### Web Crawling
- [ch_crawl.py](ch_crawl.py): Crawls Chinese web content from Xinhua News (news.cn) and People's Daily (people.com.cn)
- [en_crawl.py](en_crawl.py): Crawls English web content from the same sources

### Text Statistics
- [cal_scale.py](cal_scale.py): Calculates the scale of text corpora (number of Chinese characters and English words/letters)
- [ch_top10.py](ch_top10.py): Identifies and visualizes the top 10 most frequent Chinese characters
- [en_top10.py](en_top10.py): Identifies and visualizes the top 10 most frequent English words

### Entropy Analysis
- [cal_ch.py](cal_ch.py): Calculates and plots information entropy of Chinese characters at different sample scales
- [cal_en_letters.py](cal_en_letters.py): Calculates and plots information entropy of English letters at different sample scales
- [cal_en_words.py](cal_en_words.py): Calculates and plots information entropy of English words at different sample scales

### Zipf's Law Validation
- [zipf.py](zipf.py): Validates Zipf's Law on English text corpora:
  - Analyzes `english.news` and `en.people` corpora separately
  - Analyzes combined corpus
  - Plots word frequency rankings using logarithmic scales
  - Calculates and displays fitted line slopes

## Requirements

- Python 3.x
- Required libraries:
  ```bash
  pip install matplotlib requests beautifulsoup4 numpy
  ```

## Usage

1. **Data Collection** (if updating corpora):
   ```bash
   python ch_crawl.py  # Crawl Chinese web content
   python en_crawl.py  # Crawl English web content
   ```

2. **Statistical Analysis**:
   ```bash
   python cal_scale.py   # Calculate corpus scale
   python ch_top10.py    # Generate Chinese character Top 10 chart
   python en_top10.py    # Generate English word Top 10 chart
   ```

3. **Entropy Calculations**:
   ```bash
   python cal_ch.py         # Calculate Chinese character entropy
   python cal_en_letters.py # Calculate English letter entropy
   python cal_en_words.py   # Calculate English word entropy
   ```

4. **Zipf's Law Validation**:
   ```bash
   python zipf.py  # Validate Zipf's Law for English corpora
   ```

## Output Files

The programs generate the following chart files:
- `chinese_chars_top10.png`: Top 10 Chinese characters frequency distribution
- `english_words_top10.png`: Top 10 English words frequency distribution
- `chinese_entropy.png`: Chinese character entropy change curve
- `english_letters_entropy.png`: English letter entropy change curve
- `english_words_entropy.png`: English word entropy change curve
- `english_news_zipf_log.png`: Zipf's Law validation for English News corpus
- `en_people_zipf_log.png`: Zipf's Law validation for EN People corpus
- `combined_zipf_log.png`: Zipf's Law validation for combined corpus

## Notes

- All Python scripts use UTF-8 encoding to read files
- Ensure required libraries are installed before running the scripts
- For large datasets, adjust sample scale parameters appropriately in the code

## License

This project is for educational purposes only.

## Contact

For questions, please contact the repository owner.
