import streamlit as st
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules

st.set_page_config(page_title="Market Basket Analysis", page_icon="🛒", layout="wide")

st.title("Market Basket Analysis")
st.markdown("This app performs Market Basket Analysis using the Apriori algorithm.")


upload_file = st.file_uploader("Upload your dataset", type=["csv"])

if upload_file:
    #Read the uploaded file
    df = pd.read_csv(upload_file)
    st.success("File uploaded successfully!")

    #Show a preview of uploaded data
    st.subheader("Preview of Uploaded Data")
    st.write(df.head())

    # Check if the dataset has the required columns
    if {'Member_number','Date','itemDescription'}.issubset(df.columns):
        df_grouped = df.groupby(['Member_number', 'Date'])['itemDescription'].apply(list).reset_index()

        #Convert grouped data into a list of transactions
        transactions = df_grouped['itemDescription'].tolist()

        #Apply one-hot encoding to the transactions list
        te = TransactionEncoder()
        te_array = te.fit(transactions).transform(transactions)
        df_encoded = pd.DataFrame(te_array, columns=te.columns_)

        st.success("Transactions prepared and encoded successfully!")

        #Add sidebar sliders to set parameters
        st.sidebar.header("Set Parameters")
        min_support = st.sidebar.slider("Minimum Support", 0.001, 0.02, 0.002, step=0.001)
        min_confidence = st.sidebar.slider("Minimum Confidence", 0.1, 1.0, 0.1, step=0.5)


        #Apply apriori algorithm to find frequent itemsets
        frequent_itemsets = apriori(df_encoded, min_support = min_support, use_colnames = True)

        rules = association_rules(frequent_itemsets, metric = 'confidence', min_threshold = min_confidence)

        #Display the results
        if not rules.empty:
            rules_sorted = rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']].sort_values(by = 'lift', ascending = False)
            
            st.subheader("Top 10 Association Rules")    
            st.dataframe(rules_sorted.head(10).style.format({
                'support': '{:.3f}',
                'confidence': '{:.2f}',
                'lift': '{:.2f}'
            }))
            
            #Allow user to download all rules as csv
            csv = rules_sorted.to_csv(index = False)
            st.download_button("Download All Rules", csv, file_name = "association_rules.csv", mime = "text/csv")

        else:
            #If no rules found
            st.warning("No association rules found with the given parameters. Try adjusting the sliders.")
    else:
        #If dataset does not have the required columns
        st.error("The dataset must contain 'Member_number', 'Date', and 'itemDescription' columns.")

else:
    #If no file uploaded
    st.info("Please upload a CSV file to get started.")
            