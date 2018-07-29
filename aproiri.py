import numpy as np
import csv
import itertools
class node:
	value=1
	child={}

data=np.genfromtxt("config.csv",delimiter=",",dtype=None)

details={}
for i in data:
	details.update({i[0]:i[1]})

transcations_strings=[]
transcations=[]
sizeoneelements=set()
frequentsets=[]
frequentsetshash={}
strintoint={}
inttostring={}
support=200

def onesizefrequent():
	mydict={}
	for j in range(len(transcations)):
		for i in transcations[j]:
			if i in mydict:
				mydict[i]+=1
			else:
				mydict.update({i:1})
	for i in sizeoneelements:
		if(mydict[i]>=support):
			frequentsets.append([i])
			a=[i]
			frequentsetshash[hash(tuple(a))]=mydict[i]

def check(pos1,pos2,plen):
	for i in range(plen-1):
		if frequentsets[pos1][i]!=frequentsets[pos2][i]:
			return False
	return True


def trie_insert(inputs,maxpos):
	currnode=0
	#print inputs
	for i in range(len(inputs)):
		if inputs[i] in nodes[currnode].child:
			currnode=nodes[currnode].child[inputs[i]]
			#print "entered child node ",currnode,inputs[i]
			nodes[currnode].value+=1
		else:
			nodes[currnode].child.update({inputs[i]:int(maxpos)})
			#print "node created",currnode,"->",maxpos,inputs[i]
			nodes.append(maxpos)
			nodes[maxpos]=node()
			nodes[maxpos].child={}
			currnode=maxpos
			maxpos+=1
	return maxpos

def trie_value(ans,pos,sarray,currnode):
	if pos==len(sarray):
		ans=ans+nodes[currnode].value
		return ans
	for i in nodes[currnode].child:
		if i==sarray[pos]:
			#print "string",i,"at node ",nodes[currnode].child[i]
			ans=trie_value(ans,pos+1,sarray,nodes[currnode].child[i])
		elif i<sarray[pos]:
			#print "foun smaller",i,"than",sarray[pos],"at node ",nodes[currnode].child[i]
			ans=trie_value(ans,pos,sarray,nodes[currnode].child[i])
	return ans

def generatenew(minpos,maxpos,plen):
	for i in range(minpos,maxpos):
		for j in range(i+1,maxpos):
			if check(i,j,plen):
				new=[]
				new.extend(frequentsets[i])
				new.append(frequentsets[j][plen-1])
#				print "string is ",new
				flag=True
				size=len(new)
				k=size-1
				'''while k>=0:
					checkstr=new[0:k]+new[k+1:size]
					if hash(str(checkstr)) not in frequentsetshash:
						flag=False
						break
					k-=1
				if flag==False:
					continue'''
				mysupp=trie_value(0,0,new,0)
				if mysupp>=support:
#					print "this is frequent"
					frequentsets.append(new)
					frequentsetshash[hash(tuple(new))]=mysupp

def generateassociationrules(lhs,rhs,nume):
	#print 'LHS',lhs
	if(len(lhs)<=1):
		return 0
	#print lhs
	subsets=list(itertools.combinations(lhs,len(lhs)-1))
	#print subsets
	#print transcations
	for i in range(len(subsets)):
		#print list(subsets[i])
		first=list(subsets[i])
		first.sort()
		scnd=list(set(lhs)-set(first))
		if len(rhs)!=0:
			scnd.extend(rhs)
		scnd.sort()
		#print first,"=>",scnd
		lst=[]
		lst.extend(first)
		lst.append("=>")
		lst.extend(scnd)
		#print first
		if hash(str(lst)) in associationhashes:
			continue
		deno=frequentsetshash[hash(tuple(first))]
		#print deno
		if nume*1.0/deno>confidence:
	#		print nume*1.0/deno
			associationhashes.append(hash(str(lst)))
			for k in range(len(lst)):
					if lst[k]!="=>":
						lst[k]=inttostring[lst[k]]
			associationrules.append(lst)
	#		print "send",first,scnd
			generateassociationrules(first,scnd,nume)
	#		print "returned"
	#		print associationrules
f=open(details['input'],"r+")
lines=f.read().splitlines()
for line in lines:
	#print line
	array=line.split(',')
	for i in array:
		sizeoneelements.add(i)
	transcations_strings.append(array)
sizeoneelements=list(sizeoneelements)	
sizeoneelements.sort()
val=0
for i in sizeoneelements:
	strintoint[i]=val
	inttostring[val]=i
	val+=1
#print "hii",inttostring
for i in transcations_strings:
	lst=[]
	for j in i:
		lst.append(strintoint[j])
	transcations.append(lst)
#print transcations
for i in range(len(sizeoneelements)):
	sizeoneelements[i]=strintoint[sizeoneelements[i]]


support=len(transcations)*float(details['support'])
if int(support)<support:
	support=int(support)+1
else:
	support=int(support)
flag=int(details['flag'])
confidence=float(details['confidence'])
#print support

#print frequentsets

nodes=[]
maxpos=1
nodes.append(0)
nodes[0]=node()

for i in transcations:
	i.sort()
	maxpos=trie_insert(i,maxpos)

'''for i in range(maxpos):
	print i,nodes[i].value,nodes[i].child'''


onesizefrequent()
#print frequentsetshash
minpos=0
prvpos=len(frequentsets)
prsentlen=1
while 1:
	#print "length",prsentlen+1
	generatenew(minpos,prvpos,prsentlen)
	minpos=prvpos
	prvpos=len(frequentsets)
	prsentlen+=1
	if minpos==prvpos:
		break
#print frequentsets
#print frequentsetshash
if flag==0:
	for i in range(len(frequentsets)):
		for j in range(len(frequentsets[i])):
			frequentsets[i][j]=inttostring[frequentsets[i][j]]
	frequentsets.insert(0,[len(frequentsets)])
#	print frequentsets
	with open(details['output'], "wb") as f:
	    writer = csv.writer(f)
	    writer.writerows(frequentsets)
else:
	associationhashes=[]
	associationrules=[]
	size_of_freq=len(frequentsets)
	i=size_of_freq-1
	while i>=0:
		generateassociationrules(frequentsets[i],[],frequentsetshash[hash(tuple(frequentsets[i]))])
		i-=1
	associationrules.insert(0,[len(associationrules)])
#	print associationrules
	for i in range(len(frequentsets)):
		for j in range(len(frequentsets[i])):
			frequentsets[i][j]=inttostring[frequentsets[i][j]]
	frequentsets.insert(0,[len(frequentsets)])
	freqandassociationrules=frequentsets
	freqandassociationrules.extend(associationrules)
	print freqandassociationrules
	with open(details['output'], "wb") as f:
	    writer = csv.writer(f)
	    writer.writerows(freqandassociationrules)


