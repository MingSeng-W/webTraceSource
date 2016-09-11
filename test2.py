import time
t=time.strptime("2015-10-20 2:10",'%Y-%m-%d %H:%M')
y,m,d,h,f=t[0:5]
print y,m,d,h,f