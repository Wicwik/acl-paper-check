import pandas as pd
import ast

cee_countries = [
    "Austria",
    "Germany",
    "Bulgaria",
    "Croatia",
    "Czech Republic",
    "Hungary",
    "Poland",
    "Romania",
    "Slovakia",
    "Slovenia",
    "Estonia",
    "Latvia",
    "Lithuania"
]

df_aff = pd.read_csv("affiliations_with_countries.csv", index_col=0)
df_aff = df_aff[df_aff["country"].isin(cee_countries)]

df_papers = pd.read_csv("affiliations_per_paper.csv", index_col=0)

df_papers["affiliations"] = df_papers["affiliations"].apply(ast.literal_eval)

inst_to_country = df_aff.set_index("affiliation")["country"].to_dict()

def get_matched_countries(affiliations):
    matched_countries = {inst_to_country[aff] for aff in affiliations if aff in inst_to_country}
    return matched_countries if matched_countries else None  # None if no match

df_papers["matched_countries"] = df_papers["affiliations"].apply(get_matched_countries)

df_papers = df_papers[df_papers["matched_countries"].notnull()]

print(df_papers)

df_papers.to_csv("cee_papers.csv")