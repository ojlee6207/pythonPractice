import pandas as pd
import os
import matplotlib.pyplot as plt

plt.rc('font',family='malgun gothic')

def dataOpen():
    path = 'data/질병data/'
    file_list = os.listdir(path)
    file_list

    df = pd.DataFrame()
    keywords = ['감기','눈병','천식','피부염']

    for i in file_list:
        if i.endswith('_시도.csv'):
            # print(i)
            data = pd.read_csv(path+i, encoding='euc-kr')

            # if '감기' in i:
            #     data['구분'] = '감기'
            # elif '눈병' in i:
            #     data['구분'] = '눈병'
            # elif '천식' in i:
            #     data['구분'] = '천식'
            # elif '피부염식' in i:
            #     data['구분'] = '피부염'
            for key in keywords:
                if key in i:
                    data['구분']=key
                    break
            
            df = pd.concat([df,data])
    sido = pd.read_csv('data\질병data\시도지역코드.csv', encoding='EUC-KR')   

    return df, sido

def dataPreProcess(df,sido):
    # 시도 코드의 지역명 표시
    data_merge=pd.merge(df,sido,how='left',on='시도지역코드')
    data_merge['년/월'] = data_merge['날짜'].str[:7]
    
    dfData = data_merge[data_merge['지역명'] != '전국']
    dfData.dropna(axis=0, how='any', inplace=True)

    # 년/월, 구분별 발생건수의 평균
    yearmonthdf = dfData.groupby(['년/월','구분'],as_index=False)['발생건수(건)'].mean()

    return yearmonthdf

def dataVisualization(yearmonthdf):
    monList = yearmonthdf['년/월'].unique()
    print(f'조회 가능한 년/월 : {monList}')
    yearMonthin = input('조회 년/월 입력 >> ')
    yearMonthSearch = yearmonthdf[yearmonthdf['년/월']==yearMonthin]

    print(yearMonthSearch)

    yearMonthSearch.plot(kind='bar', x='구분', rot=0, title=yearMonthin+' 현황')
    plt.show()


if __name__ == '__main__':
    df, sido = dataOpen()
    # print(df)
    # print(sido)
    # yearmonthdf = dataPreProcess(df,sido)
    # dataVisualization(yearmonthdf)
    ab = dataPreProcess(df,sido)
    dataVisualization(ab)