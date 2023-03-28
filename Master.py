import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud
import seaborn as sns
import processor
import Analysis
import PyPDF2
import pathlib

# Main Web Design
st.sidebar.title("Loan Fraud Detection")
user_file = st.sidebar.file_uploader("Upload_file", type=['csv', 'excel', 'pdf'], accept_multiple_files=False)
if user_file is not None:
    data = pd.read_csv(user_file)
    df = processor.preprocess(data)
    st.title(':green[Loan Fraud Detection Analysis]')
    v1 = st.title(':blue[Loan Detection Data]')
    v2 = st.dataframe(df)
    total_memeber = Analysis.totalmember(df)
    st.subheader("Total Members: {}".format(total_memeber))

    # Anaysis Code
    st.title("Analysis")
    col1, col2 = st.columns(2)
    with col1:
        # Outlier Annual Income
        st.header(':green[Outlier in Annual Income]')
        st.subheader("Min Income:{0}".format(df.annual_inc.min()))
        st.subheader("Max Income:{0}".format(df.annual_inc.max()))
        fig, ax = plt.subplots()
        ax.boxplot(sorted(df['annual_inc'].tolist()))
        plt.xlabel("Outlier in Annual Income")
        st.pyplot(fig)
    with col2:
        # Outlier in Loan Amount
        st.header(':green[Outlier in Loan Amount]')
        # Finding the outier in Loan Amount
        st.subheader("Min loan:{0}".format(df.loan_amnt.min()))
        st.subheader("Max loan:{0}".format(df.loan_amnt.max()))
        fig, ax = plt.subplots()
        ax.boxplot(df['loan_amnt'])
        plt.xlabel("Outlier in Loan Amount")
        st.pyplot(fig)

    # Bivariate Analysis on NAME_CONTRACT_STATUS and AMT_CREDIT
    st.title(':green[Bivariate Analysis on Current Status and Total Payment of loan]')
    fig, ax = plt.subplots(figsize=(10, 5))
    ax = plt.gca()
    ax.plot(df['loan_status'], df['total_pymnt'], 'o', c='red', alpha=0.1)
    ax.set_xlabel('Current Status of Members')
    ax.set_ylabel('Total amount of Pyment')
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot()

    # Display those member whose current status is fully paid
    st.title(':blue[Fully Paid Loan Amount OF Members Details]')
    fully_paid = Analysis.fullypaid(df)
    st.dataframe(fully_paid)
    total_memeber = Analysis.totalmember(fully_paid)
    st.subheader("Total Members: {}".format(total_memeber))

    # univariate analysis on contract status Approved
    st.header(':green[Univariate Analysis on current status Fully Paid]')

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Pupose", "Term", "Grade", "Home_Ownership", "Corelation"])

    with tab1:
        st.header("Type of Loan")
        plt.figure(figsize=(18, 25))
        # subplot 1: loan type
        plt.subplot(4, 2, 1)
        my_plot = sns.countplot(x='purpose', palette='gist_heat_r', data=fully_paid)
        my_plot.set_xticklabels(my_plot.get_xticklabels(), rotation=90)
        plt.title("TYPES OF LOAN", size=20)
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot()

    with tab2:
        st.header("Term of Months")
        # subplot 2: Term
        plt.figure(figsize=(18, 25))
        plt.subplot(4, 2, 2)
        sns.countplot(x='term', width=0.2, palette='gist_heat_r', data=fully_paid)
        plt.title("Term of Months", size=20)
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot()

    with tab3:
        st.header("An owl")
        plt.figure(figsize=(18, 25))
        plt.subplot(4, 2, 3)
        sns.countplot(x='grade', width=0.5, palette='gist_heat_r', data=fully_paid)
        plt.title("Grade of User", size=20)
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot()
    with tab4:
        plt.figure(figsize=(18, 25))
        plt.subplot(4, 2, 4)
        sns.countplot(x='home_ownership', width=0.5, palette='gist_heat_r', data=fully_paid)
        plt.title("Home Ownership", size=20)
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot()
    with tab5:
        plt.figure(figsize=(18, 25))
        plt.subplot(4, 2, 4)
        correlation = Analysis.fullypaidcorr(df)
        sns.heatmap(correlation, linewidth=1, annot=True)
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot()

    # Display those member whose current status is Charged Off
    st.title(':blue[Charged Off Members Details]')
    charge_off = Analysis.chargedoff(df)
    st.dataframe(charge_off)
    total_memeber = Analysis.totalmember(charge_off)
    st.subheader("Total Members: {}".format(total_memeber))

    # univariate analysis on contract status Approved
    st.header(':green[Univariate Analysis on current status  Charged Off ]')
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Pupose", "Term", "Grade", "Home_Ownership", "Corelation"])

    with tab1:
        st.header("Type of Loan")
        plt.figure(figsize=(18, 25))
        # subplot 1: loan type
        plt.subplot(4, 2, 1)
        my_plot = sns.countplot(x='purpose', palette='gist_heat_r', data=charge_off)
        my_plot.set_xticklabels(my_plot.get_xticklabels(), rotation=90)
        plt.title("TYPES OF LOAN", size=20)
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot()

    with tab2:
        st.header("Term of Months")
        # subplot 2: Term
        plt.figure(figsize=(18, 25))
        plt.subplot(4, 2, 2)
        sns.countplot(x='term', width=0.2, palette='gist_heat_r', data=charge_off)
        plt.title("Term of Months", size=20)
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot()

    with tab3:
        st.header("An owl")
        plt.figure(figsize=(18, 25))
        plt.subplot(4, 2, 3)
        sns.countplot(x='grade', width=0.5, palette='gist_heat_r', data=charge_off)
        plt.title("Grade of User", size=20)
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot()
    with tab4:
        plt.figure(figsize=(18, 25))
        plt.subplot(4, 2, 4)
        sns.countplot(x='home_ownership', width=0.5, palette='gist_heat_r', data=charge_off)
        plt.title("Home Ownership", size=20)
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot()
    with tab5:
        # Correlation  matrix heat map for fully paid loan
        # st.title(':green[Correlation Heat MAP for Charged Off]')
        plt.figure(figsize=(18, 25))
        plt.subplot(4, 2, 4)
        correlation = Analysis.chargedoffcorr(df)
        sns.heatmap(correlation, linewidth=1, annot=True)
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot()


    # Display those member whose current status is Current
    st.title(':blue[Current Status Members Details]')
    current = Analysis.current_u(df)
    st.dataframe(current)
    total_memeber = Analysis.totalmember(current)
    st.subheader("Total Members: {}".format(total_memeber))

    # univariate analysis on contract status Approved
    st.header(':green[Univariate Analysis on current status  Current Memebr]')
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Pupose", "Term", "Grade", "Home_Ownership", "Corelation"])

    with tab1:
        st.header("Type of Loan")
        plt.figure(figsize=(18, 25))
        # subplot 1: loan type
        plt.subplot(4, 2, 1)
        my_plot = sns.countplot(x='purpose', palette='gist_heat_r', data=current)
        my_plot.set_xticklabels(my_plot.get_xticklabels(), rotation=90)
        plt.title("TYPES OF LOAN", size=20)
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot()

    with tab2:
        st.header("Term of Months")
        # subplot 2: Term
        plt.figure(figsize=(18, 25))
        plt.subplot(4, 2, 2)
        sns.countplot(x='term', width=0.2, palette='gist_heat_r', data=current)
        plt.title("Term of Months", size=20)
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot()

    with tab3:
        st.header("An owl")
        plt.figure(figsize=(18, 25))
        plt.subplot(4, 2, 3)
        sns.countplot(x='grade', width=0.5, palette='gist_heat_r', data=current)
        plt.title("Grade of User", size=20)
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot()
    with tab4:
        plt.figure(figsize=(18, 25))
        plt.subplot(4, 2, 4)
        sns.countplot(x='home_ownership', width=0.5, palette='gist_heat_r', data=current)
        plt.title("Home Ownership", size=20)
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot()
    with tab5:
        # Correlation  matrix heat map for fully paid loan
        # st.title(':green[Correlation Heat MAP for Charged Off]')
        plt.figure(figsize=(18, 25))
        plt.subplot(4, 2, 4)
        correlation = Analysis.chargedoffcorr(df)
        sns.heatmap(correlation, linewidth=1, annot=True)
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot()

    # Bivariate Analysis on Type of Loan  and annual income
    # st.title(':blue[Bivariate Analysis on Type of Loan  and annual income]')
    # data = df.head(20)
    # fig, ax = plt.subplots()
    # ax.bar(data['purpose'], data['annual_inc'], color='blue', width=0.5)
    # plt.xlabel("Type of Loan")
    # plt.ylabel("Annual Income")
    # plt.xticks(rotation='vertical')
    # st.pyplot(fig)

    st.title(':green[Bivariate Analysis on Type of loan and Total Payment of loan]')
    fig, ax = plt.subplots(figsize=(10, 5))
    ax = plt.gca()
    ax.plot(df['purpose'], df['total_pymnt'], 'o', c='red', alpha=0.1)
    ax.set_xlabel('Type of Loan')
    ax.set_ylabel('Total amount of Pyment')
    plt.xticks(rotation=90)
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot(fig)

    # Bivariate Analysis on NAME_CONTRACT_STATUS and AMT_CREDIT
    st.title(':blue[Bivariate Analysis on home_ownership  and Last Payment Amount]')
    fig, ax = plt.subplots(figsize=(10, 5))
    ax = plt.gca()
    ax.plot(data['home_ownership'], data['last_pymnt_amnt'], 'o', c='red', alpha=0.1)
    ax.set_xlabel('Home Ownership')
    ax.set_ylabel('Last Payment Amount of Loan')
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot()

    # Bivariate Analysis on NAME_CONTRACT_STATUS and AMT_CREDIT
    st.title(':blue[Bivariate Analysis on grade  and Total Rec. Installment]')
    fig, ax = plt.subplots(figsize=(10, 5))
    ax = plt.gca()
    ax.plot(data['grade'], data['total_rec_int'], 'o', c='red', alpha=0.1)
    ax.set_xlabel('Grade')
    ax.set_ylabel('Total Rec. Installment')
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot()