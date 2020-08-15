from django.shortcuts import render
from django.http import HttpResponse
import csv
import os
import pandas as pd
import numpy as np
from numpy import *
from django.contrib.auth.models import User,auth
from .models import DiagnosisModel
# Create your views here.
def renderPredict(request):
    symptoms=request.GET.get('symptoms')
    symptoms=symptoms.split(',')
    symptomlist=list(symptoms)
    for i in range(len(symptomlist)):
        symptomlist[i]=symptomlist[i].lower()
    with open('new_training.csv','r') as f:
        line = f.readline()
        line = line.split(',')
        allsymptoms = list(line)
        allsymptoms.pop()
        f.close()
    
    
    headers=[]
    for symptom in allsymptoms:
        headers.append(symptom)
    #Entering values for the selected Symptoms:
    selectedvalues=[usersymp for usersymp in symptomlist if usersymp in headers]
    print(selectedvalues)
    actualvalue = zeros(132)
    indices=[]
    for sv in selectedvalues:
        indices.append(headers.index(sv))
    print(indices)
    indices.sort()
    actualvalue = actualvalue.tolist()
    for i in indices:
        actualvalue.insert(i,1)
        # actualvalue=np.insert(actualvalue,i,'1')
    actualvalue = np.asarray(actualvalue)
    print('before deleting',actualvalue)
    for i in range(len(indices)):
        actualvalue=np.delete(actualvalue,len(actualvalue)-1,0)
    print('after deleting',actualvalue)
    print(len(actualvalue))
    # Dataframe Creation:
    data = [[i for i in headers],[av for av in actualvalue]]
    userdata = pd.DataFrame(data)
    
    #File checked values proper:
    # userdata.to_excel(r'C:/Users/Rudra/Desktop/user1_dataframe.xlsx',index=False,header=True)

    # #machine learning code:
     
    dataset = pd.read_csv('new_training.csv')
    x = dataset.iloc[:,:-1].values
    y = dataset.iloc[:,-1].values

    x_test = userdata.iloc[1].values


    # # #creating models:
    # from sklearn.tree import DecisionTreeClassifier
    # classifier = DecisionTreeClassifier(criterion="entropy",max_depth=10,min_samples_leaf=10)
    # classifier.fit(x,y)
    
    # from sklearn.externals import joblib
    # model = joblib.dump(classifier, 'dps_model')

    from sklearn.externals import joblib
    model = joblib.load('dps_model')



    #giving our userdata(Dataframe) for prediction:
    y_pred = model.predict([x_test])
    print(str(y_pred))
    for d in y_pred:
        key=d
        key=key.rstrip()
    print(type(key),key)

    if request.user.is_authenticated:
        userinfo = request.user.get_full_name
        diagnosisdata = DiagnosisModel(patient_name=userinfo,symtoms_entered=symptomlist,diagnosis=str(y_pred))
        diagnosisdata.save()
    else:
        diagnosisdata = DiagnosisModel(patient_name="guestuser",symtoms_entered=symptomlist,diagnosis= str(y_pred))
        diagnosisdata.save()

    #creating dictionary with descriptions of diseases:
    desc={
        'Acne':'Acne is a skin condition that occurs when your hair follicles become plugged with oil and dead skin cells.',
        'AIDS':'AIDS refers to acquired immunodeficiency syndrome. With this condition, the immune system is weakened due to HIV.',
        'Alcoholic hepatitis':'Alcoholic hepatitis is a diseased, inflammatory condition of the liver caused by heavy alcohol consumption over an extended period of time.',
        'Bronchial Asthma':'Bronchial asthma is a medical condition which causes the airway path of the lungs to swell and narrow.',
        'Allergy':'A condition in which the immune system reacts abnormally to a foreign substance.',
        'Arthritis':'Arthritis is an inflammation of the joints.It can affect one joint or multiple causing pain and stiffness that can worsen with age.',
        'Cervical spondylosis':'Cervical spondylosis is a general term for age-related wear and tear affecting the spinal disks in your neck.',
        'Chronic cholestasis':'Any condition in which the flow of bile from the liver stops or slows.Cholestasis is reduced flow of bile and can be caused by a liver infection, gallstones and cancer.',
        'Common Cold':'A common viral infection of the nose and throat. Symptoms include a runny nose, sneezing and congestion.',
        'Dengue':'A mosquito-borne viral disease occurring in tropical and subtropical areas. Symptoms include high fever, headache, rash and muscle and joint pain.',
        'Diabetes':'Diabetes is a disease that occurs when your blood glucose, also called blood sugar, is too high. Symptoms are frequent urination, increased thirst, blurry vision etc.',
        'Dimorphic hemorrhoids(piles)':'Swollen and inflamed veins in the rectum and anus that cause discomfort and bleeding.Discomfort is a common symptom, especially during bowel movements.',
        'Drug Reaction':'An adverse drug reaction (ADR) is an injury caused by taking medication. Drug allergies are a type of reaction.Skin reactions, such as hives and rashes, are the most common type.',
        'Fungal infection':"A fungus that invades the tissue can cause a disease that's confined to the skin, spreads into tissue, bones and organs or affects the whole body.",
        'Gastroenteritis':'An intestinal infection marked by diarrhoea, cramps, nausea, vomiting and fever. It is typically spread by contact with an infected person or through contaminated food or water.',
        'GERD':'Gastroesophageal Reflux Disease (GERD) is a digestive disorder that occurs when acidic stomach juices, or food and fluids back up from the stomach into the esophagus.',
        'Heart attack':'A heart attack is the death of a segment of heart muscle caused by a loss of blood supply. The blood is usually cut off when an artery supplying the heart muscle is blocked by a blood clot.',
        'Hepatitis A':'A highly contagious liver infection caused by the hepatitis A virus. It spreads from contaminated food or water or contact with someone who is infected.',
        'Hepatitis B':"A serious liver infection caused by the hepatitis B virus that's easily preventable by a vaccine. This disease is most commonly spread by exposure to infected bodily fluids.",
        'Hepatitis C':'An infection caused by a virus that attacks the liver and leads to inflammation. The virus is spread by contact with contaminated blood.',
        'Hepatitis D':'A serious liver disease caused by infection with the hepatitis D virus. Hepatitis D only occurs amongst people who are infected with the Hepatitis B virus.',
        'Hepatitis E':'A liver disease caused by the hepatitis E virus. The virus is mainly transmitted through drinking water contaminated with faecal matter.',
        'Hypertension':'Usually hypertension is defined as blood pressure above 140/90, and is considered severe if the pressure is above 180/120.',
        'Hyperthyroidism':'The overproduction of a hormone by thyroid gland. Hyperthyroidism is the production of too much thyroxine hormone. It can increase metabolism.',
        'Hypoglycemia':'Hypoglycemia is a condition in which your blood sugar (glucose) level is lower than normal. Diabetes treatment and other conditions can cause hypoglycaemia.',
        'Hypothyroidism':'Hypothyroidism is a condition in which the thyroid gland is not able to produce enough thyroid hormone.',
        'Impetigo':'A highly contagious skin infection that causes red sores on the face. Impetigo mainly affects infants and children.',
        'Jaundice':'A yellow tint to the skin or eyes caused by an excess of bilirubin, a substance created when red blood cells break down.',
        'Malaria':'A disease caused by a plasmodium parasite, transmitted by the bite of infected mosquitoes. Symptoms are chills, fever and sweating, usually occurring a few weeks after being bitten.',
        'Migraine':'A headache of varying intensity, often accompanied by nausea and sensitivity to light and sound.',
        'Osteoarthritis':'A type of arthritis that occurs when flexible tissue at the ends of bones wears down. Protective tissue at the ends of bones (cartilage) occurs gradually and worsens over time.',
        'Paralysis (brain hemorrhage)':'Paralysis is the loss of muscle function in part of your body. It happens when something goes wrong with the way messages pass between your brain and muscles.',
        'peptic ulcer disease':'A sore that develops on the lining of the oesophagus, stomach or small intestine. Ulcers occur when stomach acid damages the lining of the digestive tract.',
        'Pneumonia':'Infection that inflames air sacs in one or both lungs, which may fill with fluid.',
        'Psoriasis':'A condition in which skin cells build up and form scales and itchy, dry patches. Psoriasis is thought to be an immune system problem.',
        'Tuberculosis':'A potentially serious infectious bacterial disease that mainly affects the lungs. The bacteria that cause TB are spread when an infected person coughs or sneezes.',
        'Typhoid':'Typhoid fever is an infection that spreads through contaminated food and water. Vaccines are recommended in areas where typhoid fever is common.',
        'Urinary tract infection':'An infection in any part of the urinary system, the kidneys, bladder or urethra. These are more common in women.',
        'Varicose veins':'Gnarled, enlarged veins, most commonly appearing in the legs and feet. Varicose veins are generally benign. The cause of this condition is not known.',
        'paroxysmal positional vertigo':'Episodes of dizziness and a sensation of spinning with certain head movements, triggered by certain changes in head position.',
    }
    # if request.user.is_authenticated():
    #     return HttpResponse(request,'doctor_report.html',context={'symptom_entered':symptomlist,'diagnosis':str(y_pred)})
    
    return render(request,'predicted.html', context={'diseasename':[key],'desc':[desc[key]]})








