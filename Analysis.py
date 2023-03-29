import  pandas as pd

# Perticular User's Details
def dataframe(selected_user, df):
    if selected_user != 'overall':
        df = df[df['member_id'] == selected_user]

    return df
def totalmember(data):
    members = data['member_id'].unique().tolist()
    members.sort()
    total_members = len(members)
    return total_members

def fullypaid(data):
    fully_paid = data[data['loan_status'] == 'Fully Paid']

    return fully_paid

def chargedoff(data):
    charge_off = data[data['loan_status'] == 'Charged Off']

    return charge_off

def fullypaidcorr(data):
    fully_paid = data[data['loan_status'] == 'Fully Paid']
    correlation = fully_paid[['member_id', 'loan_amnt', 'funded_amnt', 'installment', 'total_rec_int', 'last_pymnt_amnt']].corr()

    return correlation

def chargedoffcorr(data):
    charged_off = data[data['loan_status'] == 'Charged Off']
    correlation = charged_off[['member_id', 'loan_amnt', 'funded_amnt', 'installment', 'total_rec_int', 'last_pymnt_amnt']].corr()

    return correlation

def current_u(data):
    current = data[data['loan_status'] == 'Current']
    return current

def currentcorr(data):
    current = data[data['loan_status'] == 'Charged Off']
    correlation = current[['member_id', 'loan_amnt', 'funded_amnt', 'installment', 'total_rec_int', 'last_pymnt_amnt']].corr()

    return correlation