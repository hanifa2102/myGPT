import pandas as pd

class Utility:
    @staticmethod
    def csv_to_openai(df):
        '''TODO: Non Parameterized. Takes first 2 columns,index and name of entity'''
        # sample_df=df.sample(sample_size)
        assert(df.shape[0]<=5)
        X_df_all=df.reset_index()
        # Just choose first column
        X_df=X_df_all[X_df_all.columns[0:2]]

        X=X_df.to_dict(orient='records')
        X=str(X).replace('{','{{',).replace('}','}}')

        return (X,X_df,X_df_all)