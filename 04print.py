# 02testprint.py

#변수 하나씩선언, 다중선언 가능

#a = 7
#b = 4
#ret=0

a,b,ret = 9,4,0
msg = 1234

ret = a*b

print('{} * {} = {}'.format(a,b,ret))


print('{}'.format(msg)) # 정석
print('{:0>10,}'.format(msg)) #>오른쪽맞춤 000001,234
print('{:*>10,}'.format(msg)) #*****1,234
print('{}'.format(msg))       #1,234











'''
ret = a*b
print('{} * {} = {}'.format(a,b,ret))
#print(변수, '문자', ~~) , 나열식
print(a,'*',b,'=',ret)

#print( '%d정수 %s문자열 %f실수 %c문자' %(데이터) )
print('%d * %d = %d' %(a,b,ret))


#print( f'{변수 및 값}' )
print(f'{a} * {b} = {ret}')

print()
'''