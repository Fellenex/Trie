#Trie.py
import glob
import random

#Represents a link in a Trie.
#Value is the last character assigned to the diagram (ie the transition that brought you to this state)
#Children is a list of nodes
class Node:
	def __init__(self, _value, _children, _parent=None):
		self.value = _value
		self.children = _children
		self.parent = _parent
		self.emptyChild = None
	
	def isLeaf(self):
		#isLeaf = (len(self.children) == 0) or ((len(self.children) == 1) and (self.children[0].value=='3'))
		isLeaf  = (len(self.children) == 0) and (self.value == '3')
		print "Checking leafiness of ",self.value,"(",isLeaf,")"
		return isLeaf
	
	def numDescendants(self):
		numKids = len(self.children)
		return numKids + sum([child.numDescendants() for child in self.children])
	
	def addChild(self, char):
		newChild = Node(char, [], self)
		self.children.append(newChild)
		if (char=='3'):
			self.emptyChild=newChild
		
		preSortString = ""
		postSortString = ""
		for i in range(len(self.children)):
			preSortString+=str((self.children[i]).value)+", "
		
		self.sortChildren()
		for i in range(len(self.children)):
			postSortString+=str((self.children[i]).value)+", "
		
		print "Total children: ", self.children
		print "Pre sort: "+preSortString
		print "Post sort: "+postSortString
		return newChild
	
	def sortChildren(self):
		sortedChildren = quicksort(self.children)
		self.children = sortedChildren
	
	def findChild(self, searchVal):
		nodeBinarySearch(self.children, searchVal, 0, len(self.children)-1)
		
	#The word has not been entered before, so we just append children over and over.
	def finishInsert(self, word):
		print "Adding "+word+" to ", self.value
		
		currentNode = self
		while (word != ""):
			parentNode = currentNode
			newChild = currentNode.addChild(word[0])
			currentNode = newChild
			print "Read '"+word[0]+"' and inserted "+str(currentNode.value)+" at node "+str(currentNode)+", child to "+str(parentNode)
			word = word[1:]
		
		#Return the node that should have the empty string terminator added on
		return currentNode
		
	#returns a string formed from all of the characters from the parents
	def parentString(self):
		currentNode = self
		stringSoFar = ""
		#reaching a '!' means we've hit the top
		while (currentNode.parent.value != '!'):
			stringSoFar+=str(currentNode.parent.value)
			currentNode=currentNode.parent
		return stringSoFar[::-1]



class Trie:
	def __init__(self, _root):
		#The root value should have an empty string child!
		#We use "!" to represent this.
		self.root = _root
		self.words = []
	
	def insertWord(self, word):
		print "inserting "+word
		self.words.append(word)
		currentNode = self.root
	
		if (currentNode.isLeaf()):
			#print "found leaf node, starting quick insertion"
			lastNodeInWord = currentNode.finishInsert(word)
		else:
			for i in range(len(word)):
				childExists = nodeBinarySearch(currentNode.children,word[i],0,len(currentNode.children)-1)
				
				#character doesn't exist, so none of the characters below it will exist in the trie either
				if (childExists==-1):
					lastNodeInWord = currentNode.finishInsert(word[i:])
					break
				else:
					
					#Nothing else needs to be added. This word already exists
					currentNode = currentNode.children[childExists]
					
					if (i==len(word)-1):
						lastNodeInWord=currentNode
					continue
				
			lastNodeInWord.addChild('3')
	
	def wordExists(self, word):
		currentNode = self.root
		for i in range(len(word)):
			childExists = nodeBinarySearch(currentNode.children,word[i],0,len(currentNode.children)-1)
			
			if (childExists==-1):
				#the transition for the next character doesn't exist, so none of the characters after matter
				return False
			else:
				#continue down the path, using the index given to us by the search
				currentNode = currentNode.children[childExists]
		return 
		
	def deleteWord(self, word):
		if (not(self.wordExists(word))):
			return -1
		#find the empty string terminator
		#loop:
			#check parent to see if they have only 1 child.
			#if so, continue upwards
			#else, they should be kept because they are a transition to a different word.
		#chop off the other child which leads to deletable word
	
	def numWords(self):
		#currentRoot = 
		pass
			
	def toString(self):
		subWords = []
		myStack = []
		discoveryBV = [0] * numDescendants(self.root)
		myStack.append(self.root)
		#append the current value onto each child's value
		while (len(myStack) > 0):
			currentNode = myStack.pop()
			for child in currentNode.children:
				subWords+=prependChar(self.toString, child)
			subWords = [currentNode.value]
		
		return subWords


def prependChar(addToMe, prependMe):
	prepended = []
	for word in addToMe:
		prepended=prependMe+word.value
	return prepended
			

#To be called on a list of a Trie Node's children
def quicksort(sortMe):
	if (len(sortMe) < 2):
		return sortMe
	print "Length being sorted: ",len(sortMe)
	pivot = sortMe[random.randint(0,len(sortMe)-1)]
	sortMe.remove(pivot)
	lesser = []
	greater = []
	for child in sortMe:
		if (child.value < pivot.value):
			lesser.append(child)
		else:
			greater.append(child)
	sortedLesser = quicksort(lesser)
	sortedGreater = quicksort(greater)
	return sortedLesser+[pivot]+sortedGreater

def nodeDFSSearch(searchMe, currentVertex, discoveryBV, discoveredWords):
	discoveryBV.append(currentVertex)
	discoveryBV = quicksort(discoveryBV)
	if (currentVertex.isLeaf()):
		discoveredWords.append(currentVertex.parentString())
	else:
		for child in currentVertex.children:
			print "Comparing to previously discovered nodes:"
			if (nodeBinarySearch(discoveryBV, child, 0, len(discoveryBV)-1) == -1):
				nodeDFSSearch(searchMe,child,discoveryBV,discoveredWords)
	
	return discoveredWords

#Regular binary search, meant to be run on characters
#but equally capable of being run on integers or other sorted comparables.
#Returns -1 if the element could not be found, and returns the index of the element if it could be.
def binarySearch(searchMe, character, low, high):
	if (high < low):
		return -1
	mid=(low+high)/2
	if (searchMe[mid] < character):
		#recurse on the right half
		return binarySearch(searchMe, character, mid+1, high)
	elif (searchMe[mid] > character):
		return binarySearch(searchMe, character, low, mid-1)
	else:
		return mid
		
def nodeBinarySearch(searchMe, searchValue, low, high):
	print "Binary Search Started"
	print "Searching through ", searchMe
	valuesString = ""
	for item in searchMe:
		valuesString+=str(item.value)+", "
	print "\t"+valuesString
	print "Searching for ", searchValue
	print "Searching from ", low, " to ", high
	
	mid=(low+high)/2
	
	print "Mid: ", mid
	print "SM Mid: ", (searchMe[mid]).value
	if (high < low):
		return -1
	elif (high==low):
		if (searchMe[low].value != searchValue):
			return -1
		else:
			print "Found ",searchValue," at ",low
			return low
			
	if (searchMe[mid].value < searchValue):
		#recurse on the right half
		return nodeBinarySearch(searchMe, searchValue, mid+1, high)
	elif (searchMe[mid].value > searchValue):
		return nodeBinarySearch(searchMe, searchValue, low, mid-1)
	#elif (searchMe[mid].value == searchValue):
	else:
		print "Found ",searchValue," at ",mid
		return mid

def main():
	wordList = [""]
	wordDict = {}
	#Create a tree with a root node value of !, representing the the start of the tree.
	#The '3' is used to indicate an empty transition, or finishing of a word.
	#The trie is implicitly filled with the "" word, that is the empty string.
	
	bangRoot = Node('!',[])
	bangRoot.addChild('3')
	theTrie = Trie(bangRoot)
	print "Root: ", theTrie.root, theTrie.root.value

	#for eachFile in glob.glob('words\*.txt'):
	#	theFile = open(eachFile, 'r')
	#	for line in theFile:
	#		wordList.append(line.rstrip('\n\r'))
	#	for item in wordList:
	#		theTrie.insertWord(item)
			
	#wordDict = {}.fromkeys(wordList, 0)
	
	
	trieValString=""
	for child in theTrie.root.children:
		trieValString+=str(child.value)+", "
	print "Children (pre): ", theTrie.root.children
	print "Childvals(pre): "+trieValString
	
	theTrie.insertWord("yessum");
	print "Root: ", theTrie.root.value
	trieValString=""
	for child in theTrie.root.children:
		trieValString+=str(child.value)+", "
	print "Children (post): ",theTrie.root.children
	print "Childvals(post): "+trieValString
	
	theTrie.insertWord("darling")
	theTrie.insertWord("yes")
	#theTrie.insertWord("dandy")
	#theTrie.insertWord("catastrophe")
	#theTrie.insertWord("catastrophic")
	#theTrie.insertWord("yes")
	
	print "Root: ", theTrie.root.value
	trieValString=""
	gcValString=""
	for child in theTrie.root.children:
		trieValString+=str(child.value)+", "
	print "Children (post): ",theTrie.root.children
	print "Childvals(post): "+trieValString

	
	print nodeDFSSearch(theTrie,theTrie.root,[],[])
	print theTrie.root.numDescendants()
	
	#print "toString START"
	#print theTrie.toString()
	#print "toString END"
	

#~DONE:
# File read-in
# Trie insertion
# Check if word exists
# binary search
# depth-first search
# quicksort

# Leaf determining

#~TODO:
# Trie deletion
# Trie tostring

main()