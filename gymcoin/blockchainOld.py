import hashlib
import json
from time import time
from urllib.parse import urlparse
from uuid import uuid4
import jsonpickle
import requests
from flask import Flask, jsonify, request

class Blockchain (object):

	def __init__(self):
		self.chain = [self.addGenesisBlock()];
		self.pendingTransactions = [];
		self.difficulty = 4;
		self.minerRewards = 10;
		self.blockSize = 10;

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

				newBlock = Block(transactionSlice, time());
				newBlock.prev = self.getLastBlock().hash;
				newBlock.mineBlock(self.difficulty);
				self.chain.append(newBlock);
			print("Mining Transactions Success!");

			payMiner = Transaction("Miner Rewards", miner, self.minerRewards);
			self.pendingTransactions = [payMiner];

	def addBlock(self):
		return;

	def addTransaction(self, sender, reciever, amt):
		if not sender or not reciever or not amt:
			print("transaction error 1");
			return False;

		transaction = Transaction(sender, reciever, amt);

		if not transaction.isValidTransaction():
			print("transaction error 2");
			return False;
		self.pendingTransactions.append(transaction);
		return len(self.chain) + 1;

	def getLastBlock(self):
		return self.chain[-1];

	def addGenesisBlock(self):
		t = [];
		t.append(Transaction("me", "you", 10));
		genesis = Block(t, "5");
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

class Block (object):
	def __init__(self, transactions, time):
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
		hash_string = str(self.time) + str(self.transactions) + self.milf + self.prev + str(self.nonse);
		hash_encoded = json.dumps(hash_string, sort_keys=True).encode();
		return hashlib.sha256(hash_encoded).hexdigest();

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
			if not self.transactions[i].isValidTransaction():
				return False;
			return True;

class Transaction (object):
	def __init__(self, sender, reciever, amt):
		self.sender = sender;
		self.reciever = reciever;
		self.amt = amt;
		self.time = time(); #change to current date
		self.hash = self.calculateHash();


	def calculateHash(self):
		hash_string = self.sender + self.reciever + str(self.amt) + str(self.time);
		hash_encoded = json.dumps(hash_string, sort_keys=True).encode();
		return hashlib.sha256(hash_encoded).hexdigest();

	def isValidTransaction(self):
		if(self.hash != self.calculateHash()):
			return False;
		if(self.sender == self.reciever):
			return False;
		return True;
		#needs work!

	#need to implement signing

