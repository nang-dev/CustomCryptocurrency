import hashlib
import json
from textwrap import dedent
from time import time
from uuid import uuid4
import jsonpickle
from flask import Flask
from urllib.parse import urlparse
from Crypto.PublicKey import RSA
from Crypto.Signature import *

def generateKeys():
	key = RSA.generate(2048)
	private_key = key.export_key()
	file_out = open("private.pem", "wb")
	file_out.write(private_key)

	public_key = key.publickey().export_key()
	file_out = open("receiver.pem", "wb")
	file_out.write(public_key)

	return key;

class Blockchain (object):

	def __init__(self):
		self.chain = [self.addGenesisBlock()];
		self.pendingTransactions = [];
		self.difficulty = 2;
		self.minerRewards = 10;
		self.blockSize = 10;
		self.nodes = set()

	def minePendingTransactions(self, miner):
		
		lenPT = len(self.pendingTransactions);
		if(lenPT <= 1):
			print("Not enough transactions to mine! (Must be > 1)")
		else:
			for i in range(0, lenPT, self.blockSize):

				end = i + self.blockSize;
				if i >= lenPT:
					end = lenPT;
				
				transactionSlice = self.pendingTransactions[i:end];

				newBlock = Block(transactionSlice, time(), len(self.chain));
				#print(type(self.getLastBlock()));

				hashVal = self.getLastBlock().hash;
				newBlock.prev = hashVal;
				newBlock.mineBlock(self.difficulty);
				self.chain.append(newBlock);
			print("Mining Transactions Success!");

			payMiner = Transaction("Miner Rewards", miner, self.minerRewards);
			self.pendingTransactions = [payMiner];
		
	def register_node(self, address):
		parsedUrl = urlparse(address)
		self.nodes.add(parsedUrl.netloc)
	

	def addBlock(self):
		return;

	#consensus
	def resolveConflicts(self):
		neighbors = self.nodes;
		newChain = None;

		maxLength = len(self.chain);

		for node in neighbors:
			response = requests.get(f'http://{node}/chain');

		if response.status_code == 200:
			length = response.json()['length'];
			chain = response.json()['chain'];

			if length > maxLength and self.isValidChain():
				maxLength = length;
				newChain = chain;

		if newChain:
			self.chain = newChain;
			return True;

		return False;




	def addTransaction(self, sender, reciever, amt, key):
		if not sender or not reciever or not amt:
			print("transaction error 1");
			return False;

		transaction = Transaction(sender, reciever, amt);

		transaction.signTransaction(key);

		if not transaction.isValidTransaction():
			print("transaction error 2");
			return False;
		self.pendingTransactions.append(transaction);
		return len(self.chain) + 1;

	def getLastBlock(self):
		return self.chain[-1];

	def addGenesisBlock(self):
		tArr = [];
		tArr.append(Transaction("me", "you", 10));
		genesis = Block(tArr, "5", 0);
		return genesis;

	def isValidChain(self):
		for i in range(1, len(self.chain)):
			b1 = self.chain[i-1];
			b2 = self.chain[i];

			if not b2.hasValidTransactions():
				print("error 3");
				return False;

			if b2.hash != b2.calculateHash():
				print("error 4");
				return False;


			if b2.prev != b1.hash:
				console.log("error 5");
				return False;
		return True;

	def chainJSONencode(self):

		blockArrJSON = [];
		for block in self.chain:
			blockJSON = {};
			blockJSON['hash'] = block.hash;
			blockJSON['index'] = block.index;
			blockJSON['prev'] = block.prev;
			blockJSON['time'] = block.time;
			blockJSON['nonse'] = block.nonse;
			blockJSON['milf'] = block.milf;


			transactionsJSON = [];
			tJSON = {};
			for transaction in block.transactions:
				tJSON['time'] = transaction.time;
				tJSON['sender'] = transaction.sender;
				tJSON['reciever'] = transaction.reciever;
				tJSON['amt'] = transaction.amt;
				tJSON['hash'] = transaction.hash;
				transactionsJSON.append(tJSON);

			blockJSON['transactions'] = transactionsJSON;

			blockArrJSON.append(blockJSON);

		return blockArrJSON;

	def getBalance(self, person):
		balance = 0; 
		for i in range(1, len(self.chain)):
			block = self.chain[i];
			for j in range(0, len(block.transactions)):
				transaction = block.transactions[j];
				if(transaction.sender == person):
					balance -= transaction.amt;
				if(transaction.reciever == person):
					balance += transaction.amt;
		return balance;


class Block (object):
	def __init__(self, transactions, time, index):
		self.index = index;
		self.transactions = transactions;
		self.time = time;
		self.prev = '';
		self.nonse = 0;
		self.milf = self.calculateMilf();
		self.hash = self.calculateHash();

	def calculateMilf(self):
		#scrape the pronhub milf page
		return "Kimmy Hed";
	

	def calculateHash(self):

		hashTransactions = "";

		for transaction in self.transactions:
			hashTransactions += transaction.hash;
		hashString = str(self.time) + hashTransactions + self.milf + self.prev + str(self.nonse);
		hashEncoded = json.dumps(hashString, sort_keys=True).encode();
		return hashlib.sha256(hashEncoded).hexdigest();

	def mineBlock(self, difficulty):
		arr = [];
		for i in range(0, difficulty):
			arr.append(i);
		
		#compute until the beginning of the hash = 0123..difficulty
		arrStr = map(str, arr);  
		hashPuzzle = ''.join(arrStr);
		#print(len(hashPuzzle));
		while self.hash[0:difficulty] != hashPuzzle:
			self.nonse += 1;
			self.hash = self.calculateHash();
			#print(len(hashPuzzle));
			#print(self.hash[0:difficulty]);
		print("Block Mined!");

	def hasValidTransactions(self):
		for i in range(0, len(self.transactions)):
			transaction = self.transactions[i];
			if not transaction.isValidTransaction():
				return False;
			return True;
	
	def JSONencode(self):
		return jsonpickle.encode(self);
	
class Transaction (object):
	def __init__(self, sender, reciever, amt):
		self.sender = sender;
		self.reciever = reciever;
		self.amt = amt;
		self.time = time(); #change to current date
		self.hash = self.calculateHash();


	def calculateHash(self):
		hashString = self.sender + self.reciever + str(self.amt) + str(self.time);
		hashEncoded = json.dumps(hashString, sort_keys=True).encode();
		return hashlib.sha256(hashEncoded).hexdigest();

	def isValidTransaction(self):
		if(self.hash != self.calculateHash()):
			return False;
		if(self.sender == self.reciever):
			return False;
		return True;
		#needs work!

	#need to implement signing
	def signTransaction(self, key):
		if(self.hash != self.calculateHash()):
			print("transaction tampered error");
			return False;

		if(str(key.publickey().export_key()) != self.sender):
			print("Transaction attempt to be signed from another wallet");
			return False;

		#h = MD5.new(self.hash).digest();
		pkcs1_15.new(key);
		#print(key.sign(self.hash, ""));
		print("made signature!");
		return True;