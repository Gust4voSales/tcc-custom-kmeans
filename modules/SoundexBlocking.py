import pandas as pd
import unicodedata
import fuzzy

soundex = fuzzy.Soundex(4)

class SoundexBlocking:
  blocking_key = 'blocking_key'

  def __init__(self, df: pd.DataFrame, key: str):
    self.df = df
    self.blocks: list[pd.DataFrame] = []
    self.key = key

  def __calculate_soundex(self, string: str):
    string = ''.join(filter(str.isalpha, string))
    # only ascii chars allowed to soundex lib 
    string = unicodedata.normalize('NFKD', str(string)).encode('ascii', 'ignore').decode("utf-8") 
    return soundex(string)

  def __add_soundex_key(self):
    # calculate soundex to all key (column passed) values and assign it to the SoundexBlocking.blocking_key column
    self.df[SoundexBlocking.blocking_key] = self.df[self.key].apply(self.__calculate_soundex) 


  def __divide_base_into_blocks(self):
    # Group the DataFrame based on blocking_key
    groups = self.df.groupby(SoundexBlocking.blocking_key)

    # Iterate over the groups and extract the rows
    for _, group in groups:
      self.blocks.append(group)

        
  def get_blocks(self):
    self.__add_soundex_key()
    self.__divide_base_into_blocks()

    return self.blocks
  

