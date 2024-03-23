#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import os

# Function to extract article title and text from URL
def extract_article(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        title = soup.find('title').text.strip()
        
        # Extract article text
        article_text = ''
        for paragraph in soup.find_all('p'):
            article_text += paragraph.get_text() + '\n'
        
        return title, article_text
    except Exception as e:
        print(f"Error extracting article from {url}: {str(e)}")
        return None, None

# Read URLs from the provided Excel file
input_file = "C:\\Users\\dell\\Downloads\\Input.xlsx"
df = pd.read_excel(input_file)

# Create a directory to save the extracted text files
output_directory = "extracted_articles"
os.makedirs(output_directory, exist_ok=True)

# Extract articles and save them as text files
for index, row in df.iterrows():
    url_id = row['URL_ID']
    url = row['URL']
    title, article_text = extract_article(url)
    if title and article_text:
        # Remove special characters from title to create a valid filename
        title = re.sub(r'[^\w\s]', '', title)
        # Create a text file with the URL_ID as the filename
        filename = os.path.join(output_directory, f"{url_id}_{title}.txt")
        # Write article title and text to the text file
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(title + '\n\n')
            file.write(article_text)
        print(f"Article extracted and saved: {filename}")
    else:
        print(f"Failed to extract article from URL: {url}")

print("Extraction complete.")


# In[ ]:




