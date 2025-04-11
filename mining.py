import pandas as pd
import numpy as np
import mlxtend
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

# Import raw fact table
fatality = pd.read_excel(
    "src/bitre_fatalities_dec2024.xlsx",
    sheet_name = "BITRE_Fatality",
    skiprows = 4
)

# Cleanse boolean value
fatality['Bus Involvement'] = fatality['Bus Involvement'].replace(
    {'Yes': 'Bus', 'No': 'Not Bus'}
)
fatality['Heavy Rigid Truck Involvement'] = fatality['Heavy Rigid Truck Involvement'].replace(
    {'Yes': 'Heavy Rigid Truck', 'No': 'Not Heavy Rigid Truck'}
)
fatality['Articulated Truck Involvement'] = fatality['Articulated Truck Involvement'].replace(
    {'Yes': 'Articulated Truck', 'No': 'Not Articulated Truck'}
)
fatality['Christmas Period'] = fatality['Christmas Period'].replace(
    {'Yes': 'Is Christmas', 'No': 'Not Christmas'}
)
fatality['Easter Period'] = fatality['Easter Period'].replace(
    {'Yes': 'Is Easter', 'No': 'Not Easter'}
)

# Concatenate "Speed Limit: " before speed limit value
fatality['Speed Limit'] = fatality['Speed Limit'].apply(lambda x: f"Speed Limit: {x}")

# Cleanse invalid values
invalid = [-9,'-9','Unknown','Undetermined']
fatality = fatality.replace(invalid, pd.NA)
fatality = fatality.dropna()

# Drop unconcerned columns
unconcerned = ['Crash ID', 'Time', 'Age', 'Dayweek', 'Time of day']
fatality = fatality.drop(unconcerned, axis='columns')

# Make paramater for TransactionEncoder()
list = fatality.astype(str).values.tolist()

# Covert the list to one-hot encoded boolean numpy array. 
# Apriori function allows boolean datatype only
te = TransactionEncoder()
array_te = te.fit(list).transform(list)

# Make paramater for apriori()
arm_df = pd.DataFrame(array_te, columns = te.columns_)

# Find the frequent itemsets
frequent_itemsets = apriori(arm_df,min_support=0.2,use_colnames=True)
# Check the length of rules
frequent_itemsets['length'] = frequent_itemsets['itemsets'].apply(lambda x: len(x))

# Filter with support > 0.3
frequent_itemsets[frequent_itemsets['support'] > 0.3]
# Filter with condifence > 0.5
rules_con = association_rules(frequent_itemsets, metric="confidence",min_threshold=0.5)
rules_con = rules_con.dropna()      # Cleanse "certainty_denom == 0"
# Filter with lift > 1
rules_lift = association_rules(frequent_itemsets, metric="lift",min_threshold=1)
rules_lift = rules_lift.dropna()    # Cleanse "certainty_denom == 0"

# Output
result_arm = rules_con[['antecedents','consequents','support','lift','confidence']]
road_user = ['Driver','Passenger','Motorcycle rider','Motorcycle pillion passenger','Pedal cyclist','Pedestrian']
filtered_result = result_arm[result_arm['consequents'].apply(lambda x: any(user in x for user in road_user))]
ranked_result = filtered_result.sort_values(by=['lift', 'confidence'], ascending=False)
print(ranked_result)