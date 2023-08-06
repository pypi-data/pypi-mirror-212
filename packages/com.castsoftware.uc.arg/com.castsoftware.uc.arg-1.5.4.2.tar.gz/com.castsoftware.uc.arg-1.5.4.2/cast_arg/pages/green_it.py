from cast_arg.pages.aip import AIP
from cast_arg.config import Config

from pandas import DataFrame,json_normalize,concat

class GreenIT:

    def load(cls,config:Config,domain_id,snapshot_id):
        pass

    def _get_green_rules(self,domain_id,snapshot_id):
        iso={20140522:"Green IT Index"}

        rslt_df = DataFrame()
        rslt_df.style.set_properties(subset=['text'],**{'text-align': 'left'})
        for key, value in iso.items():
            try:
                temp = DataFrame(columns=['category','violation'])
                rp = json_normalize(self.get_rules(domain_id,snapshot_id,key)['rulePattern'])
                temp['violation'] = rp['name']
                temp['category'] = value
                temp = temp.groupby(['category','violation']).size().reset_index(name='count') 

                total = temp.groupby(['category'])['count'].sum().reset_index(name='count') 
                total['violation']=''
                total = total[['category','violation','count']]

                rslt_df = concat([rslt_df,total,temp])
            except KeyError as e:
                self.warning(f'no iso rules for {value} ({e})')

        if 'category' in rslt_df.columns:
            rslt_df['category'] = rslt_df['category'].mask(rslt_df['category'].ne(rslt_df['category'].shift()).cumsum().duplicated(), '')
        else:
            self.warning('No ISO rules found')
            
        return rslt_df
