import requests
from bs4 import BeautifulSoup
import pandas as pd
import time


def get_meaning(word):
    definition = ""
    example = ""
    pos = ""
    phons = ""
    try:
        url = f"https://www.oxfordlearnersdictionaries.com/definition/english/{word.lower().strip()}"
        response = requests.get(url, headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
        })

        soup = BeautifulSoup(response.content, "html.parser")
        definition = soup.find_all("span", {"class": "def"})[0].text
        example = soup.find_all("ul", {"class": "examples"})[0].text
        pos = soup.find_all("span", {"class": "pos", "hclass": "pos"})[0].text
        phons = soup.find_all("span", {"class": "phon"})[1].text
    except:
        pass
    return pd.Series([definition, example, pos, phons], index=["definition", "example", "pos", "phons"])


if __name__ == '__main__':
    first, end = [int(item) for item in input("from to end: ").split(",")]
    time1 = time.time()
    df = pd.read_excel("main.xlsx")
    df.loc[first:end, ["definition", "example", "pos", "phons"]] = df.iloc[first:end, :]["words"].apply(get_meaning)
    df.to_excel("main.xlsx", index=False)
    print(time.time() - time1)
