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

#새로운import
import urllib.request
import json



path = './data/tour.csv'
data = pd.read_csv(path, encoding='cp949')
df = pd.DataFrame(data)
print(df)

# 열 0,1,2,3을 보기 쉽게 변환
df.columns = ['인덱스','날짜', '국가', '코드', '값']

print()
print(df)
# 데이터 타입 변환, 만약을 대비해서...
df['날짜'] = pd.to_datetime(df['날짜'], format='%Y%m')
df['값'] = pd.to_numeric(df['값'], errors='coerce')

# 그래프 그리기 - 산점도
sns.scatterplot(data=df, x='날짜', y='값')
plt.title('날짜별 값 변화')
plt.xlabel('날짜')
plt.ylabel('값')
plt.show()

# 그래프 그리기 - 선 그래프
sns.lineplot(data=df, x='날짜', y='값', marker='o')
plt.title('날짜별 값 변화 (선 그래프)')
plt.xlabel('날짜')
plt.ylabel('값')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()