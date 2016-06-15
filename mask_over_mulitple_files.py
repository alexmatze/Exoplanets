  import pyfits
  import numpy as np
  import os
  import sys  
  import scipy.ndimage as snd
  import csv
  import astropy.table
  import astropy.units as u
  import math
  import scipy.integrate as integrate
  import scipy.special as special
  from scipy.integrate import quad, dblquad
  from scipy import integrate
  
  #define function that finds radius of star
  def dist(x, y, xx, yy):
    x = x * 1.
	  y = y * 1.
	  xx = xx * 1.
  	yy = yy * 1.
  
  	return np.sqrt((yy-y)**2+(xx-x)**2) 
  
  #txt file has cor_Data files#
  data_path="cor_Data.txt"
  list_data=list(open(data_path,"r+"))
  n_data=len(list_data)
  cor_data=[]
  cor_head=[]
  
  for i in range(n_data):
  	path=list_data[i]
  	path=path.rstrip()
  	hdulist=pyfits.open(path) * 1
  	dataset=hdulist[0].data * 1
  	header=hdulist[0].header
  	cor_data.append(dataset)
  	cor_head.append(header)


  #create mask#
  for i in range(n_data):
  	mask=dataset * 1
    
  #make mask field all 0s#
  mask=np.multiply(mask,0.0)
  thrs=0.05
  
  #define x and y values#
  y_size=cor_head[0]['NAXIS1']
  x_size=cor_head[0]['NAXIS2']
  
  #for loop to define each pixel in the mask as either 1 or 0, depending on whether its luminosity#
  #is higher or lower than the threshold#
  for i in range(n_data):
  	for y in range(y_size):
  		for x in range(x_size):
  			if dataset[y,x] > thrs:
  				mask[y,x]=1
  	
  
    

  #labels where each pixel above the threshold#
  labels, num=snd.label(mask, np.ones((3,3)))
  
  #defines the center of mass for each star#
  centers = snd.center_of_mass(mask,labels,range(1,num+1))
  
  #defines the x and y values of each center of mass#
  x = np.array(centers)[:,0]
  y = np.array(centers)[:,1]
  
  #convert x and y lists into integer lists
  x=x.astype(int)
  y=y.astype(int)	
  
  #turn x and y into lists from arrays
  x=x.tolist()
  y=y.tolist()
  
  #drop the dead pixels: to-do -> x,y array
  
  def drop_dead(matrix,x1,y1):			
  	for i in range(len(x1)):		
  		if matrix[x1[i],y1[i]-1]==0 and matrix[x1[i],y1[i]+1]==0 and matrix[x1[i]+1,y1[i]]==0 and matrix[x1[i]-1,y1[i]]==0:	
  			matrix[x1[i],y1[i]] = 0
  			
  drop_dead(mask,x,y)
  
  		
  
  #define radius of stars
  radius=[]
  for i in range(len(x)):
  	x_s=x[i]
  	y_s=y[i]
  	list_x=[x_s]
  	list_y=[y_s]
  	c_list_x=[]
  	c_list_y=[]
  	n_list_x=[]
  	n_list_y=[]
  	dist_array=[]
  	for j in range(len(list_x)):
  		if list_x[j] not in c_list_x:
  			n_list_x.append(list_x[j])
  			n_list_y.append(list_y[j])
  	condition=True
  	while condition:
  		for k in range(len(n_list_x)):
  			dist_array.append(dist(n_list_x[k],n_list_y[k],x_s,y_s))	
  			if mask[n_list_x[k]+0,n_list_y[k]+1]==1:
  				list_x.append(n_list_x[k]+0)
  				list_y.append(n_list_y[k]+1)
  			if mask[n_list_x[k]+0,n_list_y[k]-1]==1:
  				list_x.append(n_list_x[k]+0)
  				list_y.append(n_list_y[k]-1)
  			if mask[n_list_x[k]+1,n_list_y[k]+0]==1:
  				list_x.append(n_list_x[k]+1)
  				list_y.append(n_list_y[k]+0)
  			if mask[n_list_x[k]-1,n_list_y[k]+0]==1:
  				list_x.append(n_list_x[k]-1)
  				list_y.append(n_list_y[k]+0)
  						
  			c_list_x.append(n_list_x[k])
  			c_list_y.append(n_list_y[k])
  			
  			
  		n_list_x=[]
  		n_list_y=[]
  	
  		for i in range(len(list_x)):
  			if list_x[i] not in c_list_x:
  				n_list_x.append(list_x[i])
  				n_list_y.append(list_y[i])
  		if len(n_list_x)==0:
  			
  			radius.append(max(dist_array))
  			condition = False
  
  #combine x,y,radius into one list
  new_radii=[]
  for r in radius:
  	if r!=0:
  		new_radii.append(r)
  coordinates_and_radii=zip(y,x,radius)
  
  print coordinates_and_radii[i]
  
  
  #create circle around each star
  area=[]
  for i in radius:
  	area.append(math.pi * i**2)
  
  
  
  #calculate for fluxes of each star
  total_flux=[]
  total=0.
  numbers1=[0,-1,-2,-3,-4,-5,-6,-7,1,2,3,4,5,6,7]
  numbers2=[0,-1,-2,-3,-4,-5,-6,-7,1,2,3,4,5,6,7]
  
  
  
  
  for i in range(len(radius)):		
  	if radius[i] > 0.:	
  		for n1 in numbers1:
  			for n2 in numbers2:
  				if dist(x[i],y[i],x[i]+n1,y[i]+n2) <= radius[i]:
  					total+=dataset[x[i]+n1,y[i]+n2]
  	total_flux.append(total)
  	total=0.
  
      
