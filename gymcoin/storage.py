def register_node(self, address):
		parsedUrl = urlparse(address)
		self.nodes.add(parsedUrl.netloc)

	#consensus algo
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
			self.chain = self.chainJSONdecode(newChain);
			print(self.chain);
			return True;

		return False;
