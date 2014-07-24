#Trie.py
import glob
import random

#To be called on a list of a Trie Nodes.
#Return Value:
	#A list of Trie nodes, sorted by their "value" variable
def nodeQuicksort(sortMe):
	if (len(sortMe) < 2):
		return sortMe
	#print "Length being sorted: ",len(sortMe)
	pivot = sortMe[random.randint(0,len(sortMe)-1)]
	sortMe.remove(pivot)
	lesser = []
	greater = []
	for child in sortMe:
		if (child.value < pivot.value):
			lesser.append(child)
		else:
			greater.append(child)
	sortedLesser = nodeQuicksort(lesser)
	sortedGreater = nodeQuicksort(greater)
	return sortedLesser+[pivot]+sortedGreater

#Searches through a list of nodes for a one where (self.value == searchValue)
#Return Values:
	# -1 if the list does not contain a node where (self.value == searchValue)
	# the index of the node where (self.value == searchValue)
def nodeBinarySearch(searchMe, searchValue, low, high):
	#print "Binary Search Started"
	#print "Searching through ", searchMe
	#valuesString = ""
	#for item in searchMe:
	#	valuesString+=str(item.value)+", "
	#print "\t"+valuesString
	#print "Searching for ", searchValue
	#print "Searching from ", low, " to ", high
	
	mid=(low+high)/2
	
	#print "Mid: ", mid
	#print "SM Mid: ", (searchMe[mid]).value
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




#Represents a link in a Trie.
#Value is the last character assigned to the diagram (ie the transition that brought you to this state)
#Children is a list of nodes
class Node:
	def __init__(self, _value, _children, _parent=None):
		self.value = _value
		self.children = _children
		self.parent = _parent
		self.emptyChild = None
		self.descendants = self.numDescendants()
		if (self.parent != None):
			self.updateAncestors(1)

	#Should never need to be used by the user. It is set at node creation
	#and incremented/decremented accordingly with insertions and deletions.
	def numDescendants(self):
		numKids = len(self.children)
		return numKids + sum([child.numDescendants() for child in self.children])
	
	#Should never need to be used by the user. It is set at node creation
	#and called accordingly with insertions and deletions.
	#It does not increase them all in one function - rather it travels upward
	#to the root and when it finds that (parent == None), it stops updating.
	#descendantChange can be negative, and should be if a node is deleted.
	def updateAncestors(self, descendantChange):
		if (self.parent == None):
			return
		else:
			currentNode = self.parent
			currentNode.descendants += descendantChange
			currentNode.updateAncestors(descendantChange)
			print currentNode.value, " now has ", currentNode.descendants, " descendants."
			
	
	def isLeaf(self):
		#isLeaf = (len(self.children) == 0) or ((len(self.children) == 1) and (self.children[0].value=='3'))
		isLeaf  = (len(self.children) == 0) and (self.value == '3')
		print "Checking leafiness of ",self.value,"(",isLeaf,")"
		return isLeaf
	
	#Creates a node with the given character as a value, and self as a parent.
	#Appends the new node to self's list of children.
	#Empty nodes are created the same way. Descendants and Ancestry are handled in __init__
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
		
		#print "Total children: ", self.children
		#print "Pre sort: "+preSortString
		#print "Post sort: "+postSortString
		return newChild
	
	#Sort the node's children in-place.
	def sortChildren(self):
		sortedChildren = nodeQuicksort(self.children)
		self.children = sortedChildren
	
	#A wrapper for nodeBinarySearch,
	#Return Values:
		#	the index of the child iff there exists a child in self.children where (child.value == searchVal)
		#	-1 otherwise
	def findChild(self, searchVal):
		return nodeBinarySearch(self.children, searchVal, 0, len(self.children)-1)
		
	#The word has not been entered before, so we just append children over and over.
	def finishInsert(self, word):
		print "Adding "+word+" to ", self.value
		
		currentNode = self
		while (word != ""):
			parentNode = currentNode
			newChild = currentNode.addChild(word[0])
			currentNode = newChild
			#print "Read '"+word[0]+"' and inserted "+str(currentNode.value)+" at node "+str(currentNode)+", child to "+str(parentNode)
			word = word[1:]
		
		#Return the node that should have the empty string terminator added on
		return currentNode
		
	#returns a string created using the character value
	#of the nodes between self and endNode (excluding the value in endNode)
	#This can be used from an empty node to create the full word
	def parentString(self,endNode):
		currentNode = self
		stringSoFar = ""
		while (currentNode.parent != endNode):
			stringSoFar+=str(currentNode.parent.value)
			currentNode=currentNode.parent
		return stringSoFar[::-1]
	
	#A wrapper for emptyNodeDFS so that the user doesn't have to initialize
	#either the discovery or discovered list.
	def emptyNodes(self):
		return self.emptyNodeDFS([],[]);
	
	#Returns a list filled with the pointers to all of the word-terminating empty nodes stored below the current vertex.
	def emptyNodeDFS(self, discoveryList, discoveredEmptyNodes):
		discoveryList.append(self)
		discoveryList = nodeQuicksort(discoveryList)
		if (self.isLeaf()):
			discoveredEmptyNodes.append(self)
		else:
			for child in self.children:
				#Compare to previously discovered nodes. If we come across a node
				#that has yet to be discovered, then it should be searched through.
				if (nodeBinarySearch(discoveryList, child, 0, len(discoveryList)-1) == -1):
					child.emptyNodeDFS(discoveryList,discoveredEmptyNodes)
		
		return discoveredEmptyNodes

	#Return a list of all of the partial subwords below this node.
	def wordsBelowMe(self):
		partialWords = []
		for emptyNode in self.emptyNodes():
			partialWords.append(emptyNode.parentString(self))
		return partialWords


class Trie:
	def __init__(self, _root):
		#The root value should have an empty string child!
		#We use "!" to represent this.
		self.root = _root
		#self.words = []
		self.emptyNodes = []
	
	def insertWord(self, word):
		print "inserting "+word
		#self.words.append(word)
		currentNode = self.root
	
		if (currentNode.isLeaf()):
			#print "found leaf node, starting quick insertion"
			lastNodeInWord = currentNode.finishInsert(word)
		else:
			for i in range(len(word)):
				childExists = nodeBinarySearch(currentNode.children,word[i],0,len(currentNode.children)-1)
				
				#character doesn't exist, so none of the characters below it will exist in the trie either
				if (childExists==-1):
					currentNode = currentNode.finishInsert(word[i:])
					break
				else:
					#Nothing else needs to be added. This character already exists
					currentNode = currentNode.children[childExists]
			
			#This statement should remain outside of the for loop.
			#It is the terminating empty node to signal that from the
			#root node until this character, as a string, forms a word.
			currentNode.addChild('3')
	
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
		return True
		
	def deleteWord(self, word):
		if (not(self.wordExists(word))):
			return -1
		#find the empty string terminator
		#loop:
			#check parent to see if they have only 1 child.
			#if so, continue upwards
			#else, they should be kept because they are a transition to a different word.
		#chop off the other child which leads to deletable word
	
	#Returns the number of words currently stored in the Trie.
	#The empty string is stored in the Trie, so if it is desired to
	#discount this string as a word, 
	def numWords(self):
		emptyStringShouldntCount = 1
		return (count(self.emptyNodeDFS) - emptyStringShouldntCount)
		
	#Display the Trie in a lovely manner.
	#Assumes a mono-spaced font.
	def toString(self):
		rootChar = self.root.value
		vSep = "|"
		hSep = "_"
		middleSpacing = self.root.descendants
		middleString = quickString(" ",middleSpacing)
		print middleString+rootChar
		for child in self.root.children:
			print (quickString(" ",middleSpacing-child.descendants))+(quickString(hSep,child.descendants))+vSep
		




def quickString(char,length):
	tempString=""
	for i in range(length):
		tempString+=char
	return tempString


#	def toString(self):
#		subWords = []
#		myStack = []
#		discoveryBV = [0] * self.root.numDescendants()
#		myStack.append(self.root)
#		#append the current value onto each child's value
#		while (len(myStack) > 0):
#			currentNode = myStack.pop()
#			for child in currentNode.children:
#				subWords+=prependChar(self.toString, child)
#			subWords = [currentNode.value]
#		
#		return subWords

#def prependChar(addToMe, prependMe):
#	prepended = []
#	for word in addToMe:
#		prepended=prependMe+word.value
#	return prepended

def main():
	wordList = [""]
	wordDict = {}
	#Create a tree with a root node value of !, representing the the start of the tree.
	#The '3' is used to indicate an empty transition, or finishing of a word.
	#The trie is implicitly filled with the "" word, that is to say the "empty string".
	print "Root: ", theTrie.root, theTrie.root.value

	#for eachFile in glob.glob('words\*.txt'):
	#	theFile = open(eachFile, 'r')
	#	for line in theFile:
	#		wordList.append(line.rstrip('\n\r'))
	#	for item in wordList:
	#		theTrie.insertWord(item)
			
	#wordDict = {}.fromkeys(wordList, 0)
	
	theTrie.insertWord("cat")
	theTrie.insertWord("cap")
	theTrie.insertWord("cam")
	theTrie.insertWord("cop")
	theTrie.insertWord("cot")
	theTrie.insertWord("coy")
	
	#trieValString=""
	#for child in theTrie.root.children:
	#	trieValString+=str(child.value)+", "
	#print "Children (pre): ", theTrie.root.children
	#print "Childvals(pre): "+trieValString
	
	#theTrie.insertWord("yessum");
	#print "Root: ", theTrie.root.value
	#trieValString=""
	#for child in theTrie.root.children:
	#	trieValString+=str(child.value)+", "
	#print "Children (post): ",theTrie.root.children
	#print "Childvals(post): "+trieValString
	
	#theTrie.insertWord("darling")
	#theTrie.insertWord("yes")
	#theTrie.insertWord("dandy")
	#theTrie.insertWord("catastrophe")
	#theTrie.insertWord("catastrophic")
	#theTrie.insertWord("yes")
	
	#print "Root: ", theTrie.root.value
	#trieValString=""
	#gcValString=""
	#for child in theTrie.root.children:
	#	trieValString+=str(child.value)+", "
	#print "Children (post): ",theTrie.root.children
	#print "Childvals(post): "+trieValString

	print theTrie.root.emptyNodes()
	print theTrie.root.numDescendants()
	oops = theTrie.root.wordsBelowMe()
	print "Words in root: ", oops
	
	print "toString START"
	print theTrie.toString()
	print "toString END"

bangRoot = Node('!',[])
bangRoot.addChild('3')
theTrie = Trie(bangRoot)

main()

#~DONE:
# File read-in
# Trie insertion
# Check if word exists
# binary search
# depth-first search
# nodeQuicksort

# Leaf determining

#~TODO:
# Trie deletion
# Trie tostring
# possible words from node. (parent string + self.value + [all of the child words]
















#Regular binary search, meant to be run on characters
#but equally capable of being run on integers or other sorted comparables.
#Returns -1 if the element could not be found, and returns the index of the element if it could be.
#def binarySearch(searchMe, character, low, high):
#	if (high < low):
#		return -1
#	mid=(low+high)/2
#	if (searchMe[mid] < character):
#		#recurse on the right half
#		return binarySearch(searchMe, character, mid+1, high)
#	elif (searchMe[mid] > character):
#		return binarySearch(searchMe, character, low, mid-1)
#	else:
#		return mid