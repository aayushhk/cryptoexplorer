import streamlit as st
from firecrawl import FirecrawlApp
from pydantic import BaseModel, Field



st.set_page_config("TxnTracker","🤖",layout="wide")
# Initialize the FirecrawlApp with your API key
def scrape(bc,tx_hash):
    print(tx_hash)
    print(bc)
    app = FirecrawlApp(api_key=st.secrets["API_KEY"])

    
        
    class ExtractSchema(BaseModel):
        transaction_hash:str
        transaction_from:str
        transaction_from_platform_app:str
        transaction_to:str
        transaction_to_platform_app:str
        amount_in_usd:str
        transaction_block_number:str
        transaction_timestamp:str
        transaction_gas_used:str
        transaction_gas_limit:str
        transaction_input:str
        transaction_output:str
        transaction_contract_address:str
    if bc=="eth":    
        bc=f'https://etherscan.io'
    elif bc=="bnb":
        bc=f'https://bscscan.com'
    
    etherscan_link = f'{bc}/tx/{tx_hash}'
    print(etherscan_link)

    data = app.scrape_url(etherscan_link, {
        'formats': ['extract'],
        'extract': {
            'schema': ExtractSchema.model_json_schema(),
        }
    })
    return data
    

TELEGRAM_BOT_TOKEN = '7900444916:AAEI2TZxgioYgjLljKj7sVuzqYkEqxhc7uw'  
TELEGRAM_CHAT_ID = '1081203414'  


def get_list():
    #read the list in txt file
    with open('watched_wallets.txt', 'r') as file:
        data = file.read().split('\n')
    return data[:-1]
def main():  
    st.title("TEAM HASH FOUNDATION")        
    st.subheader("Crypto transaction tracker")
    st.divider()
    st.sidebar.title("Actions")
    with st.sidebar:
        txn_id=st.text_area("Input Transaction hash")
        bc=st.radio("Choose Blockchain",["eth","bnb"])
        
        search=st.button("Get details")
        if search:
             st.query_params["bc"]=bc
             st.query_params["xurl"]=f"{txn_id}"
        st.divider()
        st.link_button("🤖 Add bot to your telegram",url="https://web.telegram.org/k/#@btctransactiontrackerbot",type="primary")
        st.link_button("List watched wallets",f"https://t.me/btctransactiontrackerbot?text=/list")
        
    st.query_params.setdefault("xurl", None)
    st.query_params.setdefault("bc", "eth")
    if st.query_params.values() is not None:
        tx_hash = st.query_params["xurl"]
        bc = st.query_params["bc"]
        try:
            result=scrape(bc,tx_hash)
        except Exception as e:
            st.info(f"Error occurred: Enter trxn ID to continue.")
            return
        with st.container(border=True):
            st.subheader("Transaction Hash")
            st.write(result['extract']['transaction_hash'])
        with st.container(border=True):
            st.subheader("Transaction From")
            st.code(result['extract']['transaction_from'])
            st.caption("App used: "+result['extract']['transaction_from_platform_app'])
            x= st.link_button("REMOVE from watchlist",f"https://t.me/btctransactiontrackerbot?text=/remove ETH {result['extract']['transaction_from']}")

        with st.container(border=True):
            st.subheader("Transaction To")
            st.code(result['extract']['transaction_to'])
            st.caption("App used: "+result['extract']['transaction_to_platform_app'])
            y= st.link_button("ADD to watch list",f"https://t.me/btctransactiontrackerbot?text=/add ETH {result['extract']['transaction_to']}")
        with st.container(border=True):    
            st.subheader("Amount in USD")
            st.write(result['extract']['amount_in_usd'])
        with st.container(border=True):
            st.subheader("Block Number")
            st.write(result['extract']['transaction_block_number'])
            st.subheader("Timestamp")
            st.write(result['extract']['transaction_timestamp'])
            st.subheader("Gas used")
            st.write(result['extract']['transaction_gas_used'])
            st.subheader("Gas Limit")
            st.write(result['extract']['transaction_gas_limit'])
    elif st.query_params['xurl'] is None:
         st.error("Enter transaction hash to get transaction details")
         txn_id=st.text_area("Input Transaction hash")
         search=st.button("Get details")
         if search:
             st.query_params["xurl"]=f"{txn_id}"
             st.query_params["bc"]=f"{bc}"
             
    
if __name__ == "__main__":  
    main()
