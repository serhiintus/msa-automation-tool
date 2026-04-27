import pandas as pd


class ExcelCreator:

    def __init__(self, df_columns = ["OffsetX", "OffsetY"], modules = 5, tests = 9) -> None:
        self.df_columns = df_columns
        self.modules = modules
        self.tests = tests

    def create_msa_df(self):
        self.columns_for_msa_data = {
            'Operator': [1 for i in range(self.modules*self.tests)],
            'Part': [i+1 for i in range(self.modules) for j in range(self.tests)]
        }
        self.msa_data = pd.DataFrame(self.columns_for_msa_data)

    def csv_reader(self, path):
        df = pd.read_csv(path)
        return df
    
    def data_filter(self, df, components, side):
        for i in components:
            #create a temporary dataframe
            filtered_data = pd.DataFrame(columns=self.df_columns)

            for j in range(self.modules):
                #create filter
                filt = (df["ModuleID"] == j + 1) & (df["Location Name"] == i)
                #filtered data from the .csv file and add it to the temporary dataframe
                filtered_data = pd.concat([filtered_data, df.loc[filt, self.df_columns].iloc[:9]], ignore_index=True)

            column_mapping = {
                self.df_columns[0]: f"{side}_{i}_X",
                self.df_columns[1]: f"{side}_{i}_Y"
            }
            #rename the columns and update the values of the temporary dataframe
            filtered_data = filtered_data.rename(columns=column_mapping).apply(lambda x: x/1000)
            #concatenate the MSA dataframe and the temporary dataframe with renaming columns of the temporary dataframe
            self.msa_data = pd.concat([self.msa_data, filtered_data], axis=1)

    def create_tolerance_df(self, components):
        clean_components = [component for component in components if component]
        n = len(clean_components)
        columns_with_data = {
            'Designator': clean_components,
            'Package': ['none' for i in range(n)],
            'Tolerance X': [0 for i in range(n)],
            'Tolerance Y': [0 for i in range(n)]
        }
        self.tolerance_data = pd.DataFrame(columns_with_data)

    def export_data(self):
        #export MSA and tolerance dataframes to the Excel
        with pd.ExcelWriter('MSA_data.xlsx', engine='xlsxwriter') as writer:
            self.msa_data.to_excel(writer, sheet_name='Sheet1', startrow=0, startcol=0, index=False)
            self.tolerance_data.to_excel(writer, sheet_name='Sheet1', startrow=0, startcol=len(self.msa_data.columns) + 2, index=False)
