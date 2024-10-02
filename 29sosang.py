# matplotlib=차트 
import matplotlib.pyplot as plt
import matplotlib 
import time
import numpy as np
font_name = matplotlib.font_manager.FontProperties(fname='C:/Windows/Fonts/malgun.ttf').get_name()
matplotlib.rc('font', family=font_name)
import matplotlib as mpl 
mpl.rc('axes', unicode_minus=False)
mpl.rcParams['axes.unicode_minus'] = False

import seaborn as sns 

import pandas as pd
import numpy as np
import time


path = './data/소상공인시장진흥공단_상가(상권)정보_서울_202112.csv'
df = pd.read_csv(path, encoding='utf-8')
print(df.head(10))
print()
print(df.tail(10))
print()
# print(df.info()) #컬럼열정보 
# print()

#  상권업종대분류명 

print()
cnt = df['상권업종대분류명'].value_counts()
print('상권업종대분류명', cnt)
print()
'''
상권업종대분류명 상권업종대분류명
음식             111654
소매             94320
생활서비스       58438
학문/교육        22765
부동산           14254
관광/오락        7095
스포츠           4636
숙박             2132
Name: count, dtype: int64
'''

#  상권업종대분류명  
cntidx = df['상권업종대분류명'].value_counts().index
print('상권업종대분류명', cntidx)
#['음식', '소매', '생활서비스', '학문/교육', '부동산', '관광/여가/오락', '스포츠', '숙박']


# matplotlib라이브러리  bar차트, seaborn는 barplot
sosangX = df['상권업종대분류명'].value_counts().index
sosangY = df['상권업종대분류명'].value_counts()

# plt.figure(figsize=(10,5))
# sns.barplot(x=sosangX, y=sosangY, color='green')
# plt.show()

plt.figure(figsize=(10,5))
# plt.scatter(sosangX, sosangY, marker='^')
plt.bar(sosangX, sosangY)
plt.title('상권업종대분류명  데이터출력')
plt.show()





print()



