import pandas as pd
import ast
import re

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
    "Lithuania",
]


def fix_country_format(c):
    if isinstance(c, str):
        if c[0] != "[":
            c = "[" + c + "]"

        # Find words inside brackets and add quotes
        c = re.sub(
            r"\[([^\]]+)\]",
            lambda m: "["
            + ", ".join(f'"{x.strip()}"' for x in m.group(1).split(","))
            + "]",
            c,
        )
    return c


df_aff = pd.read_csv("affiliations_with_countries.csv", index_col=0)
df_aff["country"] = df_aff["country"].apply(fix_country_format)
df_aff["country"] = df_aff["country"].apply(ast.literal_eval)
df_aff = df_aff.explode("country", ignore_index=True)

df_aff = df_aff[df_aff["country"].isin(cee_countries)]
print(df_aff)
df_papers = pd.read_csv("affiliations_per_paper.csv", index_col=0)

df_papers["affiliations"] = df_papers["affiliations"].apply(ast.literal_eval)

inst_to_country = df_aff.set_index("affiliation")["country"].to_dict()
print(inst_to_country)


def get_matched_countries(affiliations):

    return inst_to_country[affiliations[0]] if affiliations[0] in inst_to_country else None  # None if no match


df_papers["matched_countries"] = df_papers["affiliations"].apply(get_matched_countries)

df_papers = df_papers[df_papers["matched_countries"].notnull()]

print(df_papers)

df_papers.to_csv("cee_papers.csv")
