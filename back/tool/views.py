from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render , redirect
from django.core.files.storage import FileSystemStorage
import os
import pandas as pd
#from requests import post

# To upload the data ||
#                   \__/
 
def fileupload(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        print(uploaded_file)
        
        if uploaded_file.name.endswith('.csv'):
            savefile = FileSystemStorage()
            
            name = savefile.save(uploaded_file.name , uploaded_file)
            d = os.getcwd()
            
            global file_directory
            file_directory = d +'\media\\'+name
            
        return HttpResponseRedirect('/tools/display/')
            
    return render(request,'tools/upload.html')


# To display dataframe in page and about_data

def display(request):
    global data
    data = pd.read_csv(file_directory, index_col=0)
    
    # To give no.of rows and columns
    data_column = data.shape[1]
    data_row = data.shape[0]
    
    
        
    #To give name of the columns
    global c_name
    
    c_name = []
    for name in data.columns:
        c_name.append(name)
    
    #No.of null values
    count_null = []
    coun = data.isna().sum()
    for value in coun:
        count_null.append(value)
    
    # creating a dictionary to add column name with missing vaue
    global sum_col_null
    sum_col_null = {}
    for (i,j) in zip(c_name,count_null):
        sum_col_null[i] = j
    # print(sum_col_null)
    #print(c_name)
    
    
    # summary of the data
    sumar1 = data.describe().reset_index()
    #print(sumar1)
    
    return render(request,'tools/display.html', {
        
        'DataFrame':data,
        'data_column':data_column,
        'data_row':data_row,
        'col_name':c_name,
        #'null_value':[sum_col_null],
        'descr':sumar1,
        
        })


def data_clean(request):
    len_col = []

    for i in data.columns:
        ap = data[i].unique()        #getting the unique value of each columns
        len_col.append(ap)

    #print(len(len_col))
    
    
    con_var = []

    for ii in range(0,len(len_col)):
        len_var = len(len_col[ii])
        if len_var > 10:                          # Getting the numerical features by using the length of the unique value
            con_var.append(ii)
        else:
            pass

    cate_var = []

    for ii in range(0,len(len_col)):
        len_var = len(len_col[ii])
        if len_var < 10:                          # Getting the categorical value by using the length of the unique value
            cate_var.append(ii)
        else:
            pass

    col_name = []

    for ji in data.columns:                  # Getting the column names of the dataset
        col_name.append(ji)

    catevar1 = []
    for hj in cate_var:
        sd = col_name[hj]                   # To get the categorical columns from the dataframe using indexing
        catevar1.append(sd)


    constant_var = []

    for ii in range(0,len(len_col)):
        len_var = len(len_col[ii])
        if len_var ==1:                          # Getting the constant features by using the length of the unique value
            constant_var.append(ii)
        else:
            pass

    def dff(var , col_name ):
        catevar = []
        for hj in var:
            sd = col_name[hj]                   # This is the function which gives the categorical , continous feature's from the data set using index 
            catevar.append(sd)
        return catevar
    
    global categor12 , continous1
          
    categor12 = []
    continous1 = []

    for kgh in dff(con_var,col_name):
        if data[kgh].dtype == object:
            categor12.append(kgh)             #Here we find out the orginal
        else:                                 #continous features by using it's data type 
            continous1.append(kgh)
    
    for hfg in dff(cate_var,col_name):
        categor12.append(hfg)

    
#-----------------------------------------------------------------------
    
    
    noc = len(continous1)                       # To find the count of categorical and continuos 
    noco = len(categor12)                       # feature from the data set
    nocon = len(dff(constant_var , col_name))
    
    
    #print(continous1 , 'conti')
    #print(categor12 , 'cate')
        
#-----------------------------------------------------------------------
    drop_option1 = []
    if request.method == 'POST':
        
        for dfg123 in request.POST:
            if dfg123 == 'csrfmiddlewaretoken':
                pass
            else:
                drop_option1.append(dfg123)
        
              
    print(data)
    data.drop(drop_option1 , axis = 1 , inplace = True)
    #print(data)
        
    return render(request,'tools/pre.html',{
        'noc':noc,
        'noco':noco,
        'nocon':nocon,
        'nacon':continous1,
        'nacat':categor12,
        'nacons':dff(constant_var , col_name),
        'null_value':[sum_col_null],
    })
    
def data_clean2(request):
    
     
    missing_col_name = []
    
    for ii in continous1:
        if sum_col_null[ii] > 0:
            missing_col_name.append(ii)
    
    #print('missing column name ',missing_col_name)
    
    vau_fr_fil_rem = []        
    if request.method == 'POST':
        for i in missing_col_name:
            #print(i ,request.POST.get(i))
            vau_fr_fil_rem.append(request.POST.get(i))
    #print(vau_fr_fil_rem)
    
    #print(missing_col_name[0],vau_fr_fil_rem[0])
    for ii in range(0,len(vau_fr_fil_rem)):
        if vau_fr_fil_rem[ii] == '1':
            #print(missing_col_name[ii],'b')
            #print(data[missing_col_name[ii]],'b')
            meen =  round(data[missing_col_name[ii]].mean(skipna=True))
            data[missing_col_name[ii]].fillna(meen,inplace=True)
            #print(data[missing_col_name[ii]],'a')       
        else:
            data.dropna(inplace = True)
            #print(data[missing_col_name[ii]])
            #print(data[missing_col_name[ii]],'rem')
           
    
        
    
    return render(request, 'tools/pre2.html',{
        'conmiss':missing_col_name,
    })
    
def data_clean3(request):
    
    missing_cat_col_name = []
    
    for ii in categor12:
        if sum_col_null[ii] > 0:
            missing_cat_col_name.append(ii)
            
    vau_fr_fil_rem_cat = []        
    if request.method == 'POST':
        for i in missing_cat_col_name:
            #print(i ,request.POST.get(i))
            vau_fr_fil_rem_cat.append(request.POST.get(i))
    
    for ii in range(0,len(vau_fr_fil_rem_cat)):
        if vau_fr_fil_rem_cat[ii] == '1':
            print(data[missing_cat_col_name[ii]],'b')
            mod = data[missing_cat_col_name[ii]].mode(dropna=True)
            data[missing_cat_col_name[ii]].fillna(mod,inplace=True)
            print(data[missing_cat_col_name[ii]],'a')       
        else:
            data.dropna(inplace = True)
            print(data[missing_cat_col_name[ii]])

        clm_name = []
        for i in categor12:
            if data[i].dtypes == 'object':
                clm_name.append(i)
                
        for ii in clm_name:
            acul_val = data[ii].unique().tolist()
            for i in range(0,len(acul_val)):
                data[ii].replace(acul_val[i], i , inplace = True)
    
    return render(request, 'tools/pre3.html',{
        'catmiss':missing_cat_col_name,
    })
    
def ml1(request):
    
    if request.method == 'POST':
        
        global d1 , d2 
        d1 = data.drop(request.POST['ok'], axis = 1)
        d2 = data[[request.POST['ok']]]
        # d3 = d1.join(d2)
        # print(d3)
        # print(data)
        
        if request.POST['ok'] in categor12:
            return redirect('/tools/cateml/')
        else:
            return HttpResponse('numerical')
        
    
    
    return render(request, 'tools/ml1.html',{
        'inddep':c_name,
    })
    

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn import metrics
 
def cateml(request):
    X_train,X_test,y_train,y_test=train_test_split(d1,d2,train_size=0.80,random_state=0)
    
    #logisticregression
    logreg = LogisticRegression()
    logreg.fit(X_train,y_train)
    yy_pred=logreg.predict(X_test)
    
    
    #decision tree
    clf = DecisionTreeClassifier()
    clf = clf.fit(X_train,y_train)
    y_pred = clf.predict(X_test)
    
    #random forest
    clf1=RandomForestClassifier(n_estimators=100)
    clf1.fit(X_train,y_train)
    ran_pred=clf1.predict(X_test)
    
    #svm
    
    clf2 = svm.SVC(kernel='linear')
    clf2.fit(X_train, y_train)
    svm_pred = clf2.predict(X_test)
    
    #knn
    
    classifier = KNeighborsClassifier(n_neighbors=8)
    classifier.fit(X_train, y_train)
    knn_pred = classifier.predict(X_test)
    
    #gaussian
    
    model = GaussianNB()
    model.fit(X_train, y_train)
    gas_pred= model.predict(X_test)
    
    global mx_value_accuracy ,algo_grt , acur_sc , algo , ml_acr_df
    
    acur_sc = [metrics.accuracy_score(y_test, yy_pred)*100,metrics.accuracy_score(y_test, y_pred)*100
               ,metrics.accuracy_score(y_test, ran_pred)*100,metrics.accuracy_score(y_test, svm_pred)*100
               ,metrics.accuracy_score(y_test, knn_pred)*100,metrics.accuracy_score(y_test, gas_pred)*100]
    
    algo = ['logisticregression','decision tree','random forest',
            'svm','knn','gaussian']
    
    ml_acr_df = pd.DataFrame(list(zip(algo, acur_sc)), columns =['Algorithm', 'accuracy'])
    
    mx_value_accuracy = max(acur_sc)
    
    algo_grt = algo[acur_sc.index(max(acur_sc))]
    
    return redirect('/tools/cateml1/')
    
def accur(request):
    
    return render(request, 'tools/cateml.html',{
        'ml_acr_df':ml_acr_df,
        'algo':algo,
        'acr':acur_sc,
        'mx':mx_value_accuracy,
        'algo_grt':algo_grt,   
    })