import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from utils._1_Imports.svmI import *


def load_data(file_path):
    """
     Loads data from file. This is a convenience function to be used in testing
     
     @param file_path - Path to the file to load
     
     @return DataFrame with the data from the file. The columns are the names of
    """
    df = pd.read_excel(file_path)
    return df
def First_check_data(df): #Optional
    """
     First check the data. It is used to make sure there are no duplicates in the data. If it's a duplicate we'll get an error
     
     @param df - dataframe with the data
    """
    df.sample(5)
    df.info()
    df.nunique()
 
def pre_prep_data(df):
    """
     Prepares data for use. Drops and rearranges the dataframe to be ready for plotting. This is a helper function to be called by : func : ` plot_data `
     
     @param df - pandas DataFrame with columns and data
     
     @return a pandas DataFrame with columns and data ready for plotting. Columns are numbered from 0 to 7 and categorical variables
    """
    df=df.drop(['EmployeeNumber','Over18','StandardHours'],axis=1)
    #Creating numerical columns
    num_cols=['DailyRate','Age','DistanceFromHome','MonthlyIncome','MonthlyRate','PercentSalaryHike','TotalWorkingYears',
            'YearsAtCompany','NumCompaniesWorked','HourlyRate',
            'YearsInCurrentRole','YearsSinceLastPromotion','YearsWithCurrManager','TrainingTimesLastYear']

    #Creating categorical variables
    cat_cols= ['Attrition','OverTime','BusinessTravel', 'Department','Education', 'EducationField','JobSatisfaction','EnvironmentSatisfaction','WorkLifeBalance',
            'StockOptionLevel','Gender', 'PerformanceRating', 'JobInvolvement','JobLevel', 'JobRole', 'MaritalStatus','RelationshipSatisfaction']   
    print("Numerical and categorical columns succesfully created")
    return df,num_cols,cat_cols

    
def analyse_numerical_and_categorical_columns(df,num_cols,cat_cols):
    """
     Plots histogram and cross - tabulation of categorical and numerical columns. This is useful for visualizing the data that is generated by analyzing a set of data.
     
     @param df - pandas DataFrame containing the data to analyse. Should be sorted by Attrition
     @param num_cols - list of column names that are used as numerical columns
     @param cat_cols - list of column names that are used as categorical
    """
    print(df[num_cols].describe().T)
    df[num_cols].hist(figsize=(14,14))
    plt.show()
    # Print the counts of all columns in the cat_cols
    for i in cat_cols:
        print(df[i].value_counts(normalize=True))
        print('*'*40)
     #OPTIONAL FOR FURTHER ANAYLSIS
    # for i in cat_cols:
    #     if i!='Attrition':
    #         (pd.crosstab(df[i],df['Attrition'],normalize='index')*100).plot(kind='bar',figsize=(8,4),stacked=True)
    #         plt.ylabel('Percentage Attrition %')
    print(df.groupby(['Attrition'])[num_cols].mean())
    plt.figure(figsize=(15,8))
    sns.heatmap(df[num_cols].corr(),annot=True, fmt='0.2f', cmap='YlGnBu')
    plt.show()

def cleanprep_and_splitdata(df):
    """
     Takes a dataframe and cleans it for use by test_prep. This is a helper function to prepare data for testing
     
     @param df - dataframe with columns'OverTime'and'Attrition '
     
     @return pd. DataFrame with cleaned data and split data into X Y and C_s. C_s is a list
    """
    #creating list of dummy columns
    to_get_dummies_for = ['BusinessTravel', 'Department','Education', 'EducationField','EnvironmentSatisfaction', 'Gender',  'JobInvolvement','JobLevel', 'JobRole', 'MaritalStatus' ]
    #creating dummy variables
    df = pd.get_dummies(data = df, columns= to_get_dummies_for, drop_first= True)
    #mapping overtime and attrition
    dict_OverTime = {'Yes': 1, 'No':0}
    dict_attrition = {'Yes': 1, 'No': 0}
    df['OverTime'] = df.OverTime.map(dict_OverTime)
    df['Attrition'] = df.Attrition.map(dict_attrition)
    #Separating target variable and other variables
    Y= df.Attrition
    X= df.drop(columns = ['Attrition'])
    sc=StandardScaler()
    X_scaled=sc.fit_transform(X)
    X_scaled=pd.DataFrame(X_scaled, columns=X.columns)
    x_train,x_test,y_train,y_test=train_test_split(X_scaled,Y,test_size=0.2,random_state=1,stratify=Y)
    print("Train test split completed")
    return df,X,Y,x_train,x_test,y_train,y_test,X_scaled

if __name__ == "__main__":
    # Test Code: Specify the path
    file_path = 'Dataset/HR_Employee_Attrition.xlsx'
    # Test Execution: Load the data and check it
    df = load_data(file_path)
    df,num_cols,cat_cols = pre_prep_data(df)
    analyse_numerical_and_categorical_columns(df,num_cols,cat_cols)
    df,X,Y,x_train,x_test,y_train,y_test,X_scaled = cleanprep_and_splitdata(df)
