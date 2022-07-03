from django.shortcuts import render , HttpResponseRedirect , HttpResponse
import pandas as pd
import pickle as pkl
import numpy
from sklearn.tree import DecisionTreeClassifier
clf = DecisionTreeClassifier()




def bmi_(request):
    if request.method == 'POST':
        
        def bmi_calc(centi , killogram):
            meter_squar = (int(centi)*0.01)**2
            bmi = int(killogram)/meter_squar
            return bmi

        global bmi_value , avg_glucose_level , age
        bmi_value = bmi_calc(request.POST['Height'],request.POST['weight'])
        
        avg_glucose_level = request.POST['Glucose']
        age = request.POST['age']
        
        return HttpResponseRedirect('/ml/prediction/')
        
    return render(request,'ml_pred/ml_bmi_cal_form.html')

def prediction(request):
    if request.method == 'POST':
        
        
        model_col_name = ['gender', 'age', 'hypertension', 'heart_disease', 'ever_married',
       'work_type', 'Residence_type', 'avg_glucose_level', 'bmi',
       'smoke_status']
        

        ml_values = [int(request.POST['gender']), int(age) ,int(request.POST['hypertension'])
                           ,int(request.POST['heart_disease']),int(request.POST['ever_married']),
                           int(request.POST['work_type']),int(request.POST['Residence_type']),
                           int(avg_glucose_level), bmi_value , int(request.POST['smoke_status'])]
        
        
        dataf = pd.DataFrame([ml_values],columns=model_col_name)
        
        # [1.0, 80.0, 0.0, 1.0, 1.0, 1.0, 1.0, 105.92, 32.5, 0.0] 
         
        with open('ml_decision', 'rb') as f:
            mod = pkl.load(f)
            
        print(mod.predict(dataf))
        
        pred = mod.predict(dataf)
        
        out = 'not having stroke'
        
        if pred == 1:
            out = 'Having heart stroke'
            
        return render(request,'ml_pred/output.html',{
        'output':out,
        })
        
    return render(request,'ml_pred/ml_form.html')

