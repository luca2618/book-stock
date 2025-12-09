import pandas as pd
from bs4 import BeautifulSoup
import requests
# import wait function to avoid rate limiting
from time import sleep
from tqdm import tqdm
def scrape_most_popular_reviews():
    books = pd.read_csv('./data/books.csv')

    most_popular_reviews = pd.DataFrame(columns=["goodreads_book_id", "score","date","review_text"])

    for index, row in tqdm(books.iterrows(), total=books.shape[0]):
        sleep(1)  # sleep for 1 second to avoid rate limiting
        book_id = row['goodreads_book_id']
        url = f'https://www.goodreads.com/book/show/{book_id}'
        
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            # fetch elements with class "ReviewCard"
            review_cards = soup.find_all(class_='ReviewCard')
            for review in review_cards:
                try:
                    #seperate review text from class "ReviewText"
                    review_text = review.find(class_='ReviewText')
                    review_text = review_text.get_text(strip=True)
                    #clean review text by removing newline characters and line separators
                    review_text = review_text.replace('\n', ' ').replace('\r', ' ')

                    #fetch date from class "Text Text__body3"
            
                    date_elem = review.find(class_='Text Text__body3')
                    date = date_elem.get_text(strip=True).lower().replace(',', '')
                    month, day, year = date.split(' ')
                    # Get review score from class "RatingStars RatingStars__small"
                    # take the aria-label attribute, which is a string formmated as "Rating x out of 5"
                    rating_stars = review.find(class_='RatingStars RatingStars__small')
                    rating = rating_stars['aria-label']
                    rating = rating.split(' ')[1]  # extract the number part

                    most_popular_reviews.loc[len(most_popular_reviews)] ={
                        "book_id": book_id,
                        "score": rating,
                        "date": f"{month}/{day}/{year}",
                        "review_text": review_text
                    }
                except Exception as e:
                    print("Error parsing review:", e)
        if index % 1000 == 0:
            most_popular_reviews.to_csv('./data/most_popular_reviews'+str(index)+'.csv', index=False)


if __name__ == "__main__":
    scrape_most_popular_reviews()
        
        