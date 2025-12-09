# merge folder of most_popular_reviews csv files into one
import pandas as pd
import os
def merge_most_popular_reviews(input_folder='./data/', output_file='./data/most_popular_reviews_merged.csv'):
    all_files = [f for f in os.listdir(input_folder) if f.startswith('most_popular_reviews') and f.endswith('.csv')]
    df_list = []
    for file in all_files:
        df = pd.read_csv(os.path.join(input_folder, file))
        df_list.append(df)
    merged_df = pd.concat(df_list, ignore_index=True)
    merged_df.to_csv(output_file, index=False)

merge_most_popular_reviews()