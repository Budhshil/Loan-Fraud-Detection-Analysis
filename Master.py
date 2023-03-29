import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
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

        st.write("It can be seen that Income of client has outlier of annual_inc column")
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

        #print concluion
        st.write('It can be seen that loan amount of memeber has outlier of loan_amnt column, it can be seen the three Quartile in boxplot. Median is the center of boxplot line.')

    # Bivariate Analysis on NAME_CONTRACT_STATUS and AMT_CREDIT
    st.title(':green[Bivariate Analysis on Current Status and Total Payment of loan]')
    fig, ax = plt.subplots(figsize=(10, 5))
    ax = plt.gca()
    ax.plot(df['loan_status'], df['total_pymnt'], 'o', c='red', alpha=0.1)
    ax.set_xlabel('Current Status of Members')
    ax.set_ylabel('Total amount of Pyment')
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot()

    #Conclusion
    st.write("Bivariate Analysis is used to find out is there is relationship between two sets of values.")
    st.write("It can clearly seen that total payment and current status of memebr for loan, who has more paid the loan Amount shows intrest for loan")

    # Display those member whose current status is fully paid
    st.title(':blue[Fully Paid Loan Amount OF Members Details]')
    fully_paid = Analysis.fullypaid(df)
    st.dataframe(fully_paid)
    total_memeber = Analysis.totalmember(fully_paid)
    st.subheader("Total Members: {}".format(total_memeber))

    # univariate analysis on contract status Approved
    st.header(':green[Univariate Analysis on current status Fully Paid]')

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Pupose", "Term", "Grade", "Home_Ownership", "Verification","Corelation"])

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

        #conclustion
        st.write("It can be seen that applicant majorly apply for debt_consolidation i.e: 10,000 approx. applicant")
    with tab2:
        st.header("Term of Months")
        # subplot 2: Term
        plt.figure(figsize=(18, 25))
        plt.subplot(4, 2, 2)
        sns.countplot(x='term', palette='gist_heat_r', data=fully_paid)
        plt.title("Term of Months", size=20)
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot()

        # conclustion
        st.write("It can be seen that applicant majorly take a loan  for 36 months whose current status is Fully Paid i.e: 17,000 approx. applicant")

    with tab3:
        st.header("Grade")
        plt.figure(figsize=(18, 25))
        plt.subplot(4, 2, 3)
        sns.countplot(x='grade', palette='gist_heat_r', data=fully_paid)
        plt.title("Grade of User", size=20)
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot()

        # conclustion
        st.write("It can be seen that majorly applicant is Grade B , A ,C  who taking loan")

    with tab4:
        plt.figure(figsize=(18, 25))
        plt.subplot(4, 2, 4)
        sns.countplot(x='home_ownership', palette='gist_heat_r', data=fully_paid)
        plt.title("Home Ownership", size=20)
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot()

        # conclustion
        st.write("It can be seen that applicant whose paying rent they apply highest loan")

    with tab5:
        plt.figure(figsize=(18, 25))
        plt.subplot(4, 2, 4)
        sns.countplot(x='verification_status', palette='gist_heat_r', data=fully_paid)
        plt.title("Home Ownership", size=20)
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot()

    with tab6:
        plt.figure(figsize=(18, 25))
        plt.subplot(4, 2, 4)
        correlation = Analysis.fullypaidcorr(df)
        sns.heatmap(correlation, linewidth=1, annot=True)
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot()
        st.write("The figure Shown here is the heat map of Correlation matrix of Various Attributes")

    #Conclusion of Fully paid data
    st.header(':green[Conclusion of Fully paid data:]')
    st.write("Most  of the Loan application are debt_consolidation")
    st.write("Most of the application taking time period is 36 months")
    st.write("It can be seen that client verification status is NOT-VERIFIED they apply more loan for compare verified member")

    # Display those member whose current status is Charged Off
    st.title(':blue[Charged Off Members Details]')
    charge_off = Analysis.chargedoff(df)
    st.dataframe(charge_off)
    total_memeber = Analysis.totalmember(charge_off)
    st.subheader("Total Members: {}".format(total_memeber))

    # univariate analysis on contract status Approved
    st.header(':green[Univariate Analysis on current status  Charged Off ]')
    tab1, tab2, tab3, tab4,tab5, tab6 = st.tabs(["Pupose", "Term", "Grade", "Home_Ownership","Verified Member", "Corelation"])

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
        # conclustion
        st.write("It can be seen that applicant majorly apply for debt_consolidation i.e: 16,000 approx. applicant")

    with tab2:
        st.header("Term of Months")
        # subplot 2: Term
        plt.figure(figsize=(18, 25))
        plt.subplot(4, 2, 2)
        sns.countplot(x='term', palette='gist_heat_r', data=charge_off)
        plt.title("Term of Months", size=20)
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot()
        # conclustion
        st.write("It can be seen that applicant majorly take a loan  for 36 months whose current status is Charge off")
    with tab3:
        plt.figure(figsize=(18, 25))
        plt.subplot(4, 2, 3)
        sns.countplot(x='grade', palette='gist_heat_r', data=charge_off)
        plt.title("Grade of User", size=20)
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot()
        # conclustion
        st.write("It can be seen that majorly applicant is Grade B , C ,D  who taking loan")
    with tab4:
        plt.figure(figsize=(18, 25))
        plt.subplot(4, 2, 4)
        sns.countplot(x='home_ownership', palette='gist_heat_r', data=charge_off)
        plt.title("Home Ownership", size=20)
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot()
        # conclustion
        st.write("It can be seen that applicant whose paying rent they apply highest loan")
    with tab5:
        plt.figure(figsize=(18, 25))
        plt.subplot(4, 2, 4)
        sns.countplot(x='verification_status', palette='gist_heat_r', data=charge_off)
        plt.title("Home Ownership", size=20)
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot()

    with tab6:
        # Correlation  matrix heat map for fully paid loan
        # st.title(':green[Correlation Heat MAP for Charged Off]')
        plt.figure(figsize=(18, 25))
        plt.subplot(4, 2, 4)
        correlation = Analysis.chargedoffcorr(df)
        sns.heatmap(correlation, linewidth=1, annot=True)
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot()
        st.write("The figure Shown here is the heat map of Correlation matrix of Various Attributes")

        # Conclusion of Fully paid data
    st.header(':green[Conclusion of Charge Off data:]')
    st.write("Most  of the Loan application are debt_consolidation")
    st.write("Most of the application taking time period is 36 months but not paying loan amount")
    st.write("It can be seen that client verification status is NOT-VERIFIED they apply for loan , also VERIFIED member's apply for loan but both are not paying loan amount")


    # Display those member whose current status is Current
    st.title(':blue[Current Status Members Details]')
    current = Analysis.current_u(df)
    st.dataframe(current)
    total_memeber = Analysis.totalmember(current)
    st.subheader("Total Members: {}".format(total_memeber))

    # univariate analysis on contract status Approved
    st.header(':green[Univariate Analysis on current status  Current Memebr]')
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Pupose", "Term", "Grade", "Home_Ownership","Verification Member", "Corelation"])

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
        # conclustion
        st.write("It can be seen that applicant majorly apply for debt_consolidation i.e: 350 approx. applicant")
    with tab2:
        st.header("Term of Months")
        # subplot 2: Term
        plt.figure(figsize=(18, 25))
        plt.subplot(4, 2, 2)
        sns.countplot(x='term', palette='gist_heat_r', data=current)
        plt.title("Term of Months", size=20)
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot()
        # conclustion
        st.write("It can be seen that applicant take a loan for 60 months whose current status is Current")
    with tab3:
        st.header("An owl")
        plt.figure(figsize=(18, 25))
        plt.subplot(4, 2, 3)
        sns.countplot(x='grade', palette='gist_heat_r', data=current)
        plt.title("Grade of User", size=20)
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot()
        # conclustion
        st.write("It can be seen that majorly applicant  Grade is B and C")
    with tab4:
        plt.figure(figsize=(18, 25))
        plt.subplot(4, 2, 4)
        sns.countplot(x='home_ownership', palette='gist_heat_r', data=current)
        plt.title("Home Ownership", size=20)
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot()
        # conclustion
        st.write("It can be seen that applicant whose paying Mortage they apply highest loan")

    with tab5:
        plt.figure(figsize=(18, 25))
        plt.subplot(4, 2, 4)
        sns.countplot(x='verification_status', palette='gist_heat_r', data=current)
        plt.title("Home Ownership", size=20)
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot()

    with tab6:
        # Correlation  matrix heat map for fully paid loan
        # st.title(':green[Correlation Heat MAP for Charged Off]')
        plt.figure(figsize=(18, 25))
        plt.subplot(4, 2, 4)
        correlation = Analysis.chargedoffcorr(df)
        sns.heatmap(correlation, linewidth=1, annot=True)
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot()
        st.write("The figure Shown here is the heat map of Correlation matrix of Various Attributes")

        # Conclusion of Fully paid data
    st.header(':green[Conclusion of Memebrs Status is Current:]')
    st.write("Most  of the Loan application are debt_consolidation")
    st.write("Application taking time period is 60 months")
    st.write("It can be seen that client verification status is VERIFIED they apply more for loan")

    #Bivariate Analysis
    st.title(':green[Bivariate Analysis on Type of loan and Total Payment of loan]')
    fig, ax = plt.subplots(figsize=(10, 5))
    ax = plt.gca()
    ax.plot(df['purpose'], df['total_pymnt'], 'o', c='red', alpha=0.1)
    ax.set_xlabel('Type of Loan')
    ax.set_ylabel('Total amount of Pyment')
    plt.xticks(rotation=90)
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot(fig)

    # Conclusion
    st.write("Bivariate Analysis is used to find out is there is relationship between two sets of values.")
    st.write("It can clearly seen that home_improvement and deb_consolidation loan type memeber are paid highst total payment of laon.")

    # Bivariate Analysis on NAME_CONTRACT_STATUS and AMT_CREDIT
    # st.title(':blue[Bivariate Analysis on home_ownership  and Last Payment Amount]')
    # fig, ax = plt.subplots(figsize=(10, 5))
    # ax = plt.gca()
    # ax.plot(data['loan_amnt'], data['total_pymnt'], 'o', c='red', alpha=0.1)
    # ax.set_xlabel('Annual Income')
    # ax.set_ylabel('total Amount')
    # st.set_option('deprecation.showPyplotGlobalUse', False)
    # st.pyplot()
    # Bivariate analysis on Income & Credit Amount
    st.title(':blue[Bivariate Analysis on total_rec_int  and loan Amount]')
    fig, ax = plt.subplots(figsize=(10, 5))
    ax = plt.gca()
    ax.scatter(df['total_rec_int'], df['loan_amnt'], c='orange')
    ax.set_xlabel('Total Recovery Installment')
    ax.set_ylabel('Loan amount')
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot()

    #conclusion:
    st.write("We can seen that whose total_rec_int is above 5000 they apply 15000 amount of loan.")

    # Bivariate Analysis on NAME_CONTRACT_STATUS and AMT_CREDIT
    st.title(':blue[Bivariate Analysis on grade  and Total Rec. Installment]')
    fig, ax = plt.subplots(figsize=(10, 5))
    ax = plt.gca()
    ax.plot(data['grade'], data['total_rec_int'], 'o', c='red', alpha=0.1)
    ax.set_xlabel('Grade')
    ax.set_ylabel('Total Rec. Installment')
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot()

    st. write("we can seen that whose Grade is F, D and F those recovery amount approx. 10,000 ")

    #Final Conclusion
    st.title(':green[Conclusion]')
    st.write("Most of the loan applications are for debt_consolidation loans which is around 12,100")
    st.write("Most of the application taking time period is 36 months")
    st.write("It can be seen that most VERIFIED clint  are not labeled as 'defaulted'")
    st.write("To,Approved the Loan it is a most important variable to decide loan is approved or not")