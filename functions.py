import numpy as np

#Makes each values in a dict lowercase
def _lowercase(obj):
    if isinstance(obj, dict):
        return {k.lower():_lowercase(v) for k, v in obj.items()}
    elif isinstance(obj, (list, set, tuple)):
        t = type(obj)
        return t(_lowercase(o) for o in obj)
    elif isinstance(obj, str):
        return obj.lower()
    else:
        return obj
    
def explodeSkill(dataF):
    dataF.loc[:, 'skills_split'] = dataF['Skills'].str.split(',')

    #Explode the resulting lists into separate rows
    dataF = dataF.explode('skills_split')

    #Strip any leading/trailing whitespace from the skills
    dataF['skills_split'] = dataF['skills_split'].str.strip()
    dataF.replace('', np.nan, inplace=True)
    dataF.dropna(inplace=True)
    return dataF

#Explode by Job Cata
def explodeSkillCata(dataF, jobTitle):
    #Filter based on JobTitle 
    dataF = dataF[dataF.Classification.isin([jobTitle])]
    return explodeSkill(dataF)

def getTopXSkill(dataF, x):
    if (isinstance(x , int)):
        #Count the occurrences of each skill
        skill_counts = dataF['skills_split'].value_counts()

        #Get the top 20 skills
        top_20_skills_sg = skill_counts.head(x).reset_index()
        top_20_skills_sg.columns = ['Skill', 'Count']
        return top_20_skills_sg
    else:
        print("Invalid number")
        
        

#Group Skills into Catagory
def catagoriseSkills(dataF):
    #Skills Groups
    catagoriesDict = {"Programming Languages": ["Java", "Python", "C++", "C#", "VB.NET", "R", "BASIC","JavaScript","HTML","HTTP", "CSS","ASP.NET", "PHP","jQuery","AJAX","SQL", "NoSQL","GO"],
              "Frameworks & Library":[".NET", "Angular", "AngularJS", "Bootstrap", "Node.js", "Express", "j2EE", "WebSphere", "Citrix",'AWS',"React","Backend","software","Web","NIST"],
              "Project Management": ["Project Management", "Development Manager", "IT Manager","communication", "Business Analyst", "Agile", "Scrum", "Collaboration", "TDD", "SDLC", "Consulting","Management","Project","DevOps","Application", "Risk Management"],
              "Data Management/Analytics": ["Data Analysis", "Data Architecture", "Data Analytics", "Big Data", "Machine Learning", "Statistical Analysis","Analysis","Architecture","Oracle","Database"],
              "Development/Testing": ["Testing", "Development","Test Case","Test","Black Box","White Box","Git","GitHub","Software Development","Firewall","Windows","Linux","Systems"]
            }
    parentList = []
    catagoriesDict = _lowercase(catagoriesDict)
    for skills in dataF['Skill']:
        cataFound = False
        #print(skills)
        for catagory in catagoriesDict:
            #print(skills)
            if skills in catagoriesDict[catagory]:
                #print(catagory)
                parentList.append(catagory)
                cataFound = True
                break
            else:
                cataFound=False
    
        if (not cataFound):
            #print("Not Found")
            parentList.append('Others')
    return parentList