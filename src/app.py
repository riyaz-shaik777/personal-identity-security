from flask import Flask,render_template,redirect,request,session
from web3 import Web3,HTTPProvider
import json

def connect_with_register_blockchain(acc):
    blockchain='http://127.0.0.1:7545' # step - 1: pass blockchain server details

    web3=Web3(HTTPProvider(blockchain)) # step - 2: Connecting through HTTP Provider of Web3

    if acc==0: # step - 3: loading the account details
        acc=web3.eth.accounts[0] # primary account, if no account is mentioned
    web3.eth.defaultAccount=acc # account is needed because we have to make money transactions

    artifact_path="../build/contracts/register.json" # step - 4: loading the register artifact
    with open(artifact_path) as f:
        contract_json=json.load(f) # string into json object
        contract_abi=contract_json['abi'] # application binary interface
        contract_address=contract_json['networks']['5777']['address']
    
    contract=web3.eth.contract(address=contract_address,abi=contract_abi) # step - 5: connect with contract

    return (contract,web3)

# launch web app
app=Flask(__name__)

@app.route('/')
def homePage():
    return render_template('index.html')

@app.route('/registerUser',methods=['post']) # route to create account in platform
def registerUser(): 
    username=request.form['username'] # step-1: collect details from HTML Form
    name=request.form['name']
    password=request.form['password']
    email=request.form['email']
    mobile=request.form['mobile']
    print(username,name,password,email,mobile)

    try:
        contract,web3=connect_with_register_blockchain(0) # step - 2: connecting with blockchain
        tx_hash=contract.functions.registerUser(username,name,int(password),email,mobile).transact() # step - 3: making contract call
        web3.eth.waitForTransactionReceipt(tx_hash) # step - 4: wait until block is added to chain
        return render_template('index.html',res='Registered Successfully')
    except:
        return render_template('index.html',err='You have already registered')

@app.route('/loginUser',methods=['post'])
def loginUser():
    username=request.form['username1']
    password=request.form['password1']
    print(username,password)

    try:
        contract,web3=connect_with_register_blockchain(0)
        state=contract.functions.loginUser(username,int(password)).call()
        if state==True:
            return render_template('index.html',res1='Login Valid')
        else:
            return render_template('index.html',err1='Invalid Credentials')
    except:
        return render_template('index.html',err1='First register Account')

if __name__=="__main__":
    app.run(port=5001,host='0.0.0.0',debug=True)