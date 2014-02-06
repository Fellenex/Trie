#Trie.py
import glob

class Trie:
	def __init__(self, _root):
		#The root value should be the empty string!
		#We use "3" to represent this.
		self.root = _root
	
	def insertWord(self, _node, word):
		node = _node
		for char in word:
			i=0
			found = False
			if len(node.children) == 0:
				node = node.addChild(char)
				continue
			else:
				while not(found):
					if i >= len(node.children):
						#i has been incremented too many times.
						#Break out of this loop!
						break
					if (char == node.children[i].value):
						#This transition has already been added to our Trie!
						node = node.children[i]
						found = True
					i+=1
			
			if not(found):
				#This character transition has not been established yet in the Trie
				#Once the function gets to this point,  it will skip the
				#while loop above every time and come straight here, adding
				#the characters quickly without checking for transitions since there won't be any
			
				#If this character has not been added, then all of the characters
				#after this character have not been added. Finish out the addition quickly!
				node = node.addChild(char)
			
	
	def toString(self, _node=None):
		#Can't set default values to the root from the constructor
		#because it references self, so we put a dummy Null value in and
		#use a typecheck to initiate the toString
		if (_node == None):
			_node = self.root
		print _node.value
		for child in _node.children:
			self.toString(child)

#Represents a link in a Trie.
#Value is the last character assigned to the diagram (ie the transition that brought you to this state)
#Children is a list of nodes
class Node:
	def __init__(self, _value, _children):
		self.value = _value
		self.children = _children
	
	def isLeaf(self):
		return (children == [])
	
	def numChildren(self):
		numKids = len(self.children)
		return numKids + sum([child.numChildren() for child in self.children])
	
	def addChild(self, char):
		temp = Node(char, [])
		self.children.append(temp)
		return temp


#Regular binary search, meant to be run on characters
#but equally capable of being run on integers or other sorted comparables.
#Returns -1 if the element could not be found, and returns the index of the element if it could be.
def binarySearch(searchMe, character, low, high):
	if (high < low):
		return -1
	mid=(low+high)/2
	if (searchMe[mid] < character):
		#recurse on the right half
		return charBinarySearch(searchMe, character, mid+1, high)
	elif (searchMe[mid] > character):
		return charBinarySearch(searchMe, character, low, mid-1)
	else:
		return mid
		
def main():
	wordList = []
	wordDict = {}
	#Create a tree with a root node equal to 3, representing the empty string
	theTrie = Trie(Node('3', []))

	for eachFile in glob.glob('words\*.txt'):
		theFile = open(eachFile, 'r')
		for line in theFile:
			wordList.append(line.rstrip('\n\r'))
		for item in wordList:
			theTrie.insertWord(theTrie.root, item)
			
	wordDict = {}.fromkeys(wordList, 0)
	
	theTrie.toString()
	
	#for child in theTrie.root.children:
	#	print child.numChildren()
	

#~DONE:
# File read-in
# Trie insertion
# Children counting
# Leaf determining

#~TODO:
# Trie deletion

main()