import numpy as np

# Define a common color map for categories
category_colors = {
  "programming languages": "#636EFA",
  "frameworks & library": "#EF553B",
  "project management": "#00CC96",
  "data management/analytics": "#AB63FA",
  "development/testing": "#FFA15A",
  "others": "#19D3F3",
  "certifications": "#FF6692"
}

#Makes each values lowercase, works for most class
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
#Return Dataframe for skills based on total number of each skills    
def explodeSkill(dataF):
    dataF.loc[:, 'skills_split'] = dataF['Skills'].str.split(',')

    #Explode the resulting lists into separate rows
    dataF = dataF.explode('skills_split')

    #Strip any leading/trailing whitespace from the skills
    dataF['skills_split'] = dataF['skills_split'].str.strip()
    #Incase there are empty rows delete them
    dataF.replace('', np.nan, inplace=True)
    dataF.dropna(inplace=True)
    return dataF

#Explode by Job Cata
def explodeSkillCata(dataF, jobTitle):
    #Filter based on JobTitle 
    dataF = dataF[dataF.Classification.isin([jobTitle])]
    return explodeSkill(dataF)

#Return set amount of skills based on the input
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
              "Frameworks & Library":[".NET", "Angular", "AngularJS", "Bootstrap", "Node.js", "Express", "j2EE", "WebSphere", "Citrix",'AWS',"React","Backend","software","Web","NIST","Azure","Cloud"],
              "Project Management": ["Project Management", "Development Manager", "IT Manager","communication", "Business Analyst", "Agile", "Scrum", "Collaboration", "TDD", "SDLC", "Consulting","Management","Project","DevOps","Application", "Risk Management","Leadership"],
              "Data Management/Analytics": ["Data Analysis", "Data Architecture", "Data Analytics", "Big Data", "Machine Learning", "Statistical Analysis","Analysis","Architecture","Oracle","Database","API"],
              "Development/Testing": ["Testing", "Development","Test Case","Test","Black Box","White Box","Git","GitHub","Software Development","Firewall","Windows","Linux","Systems","Mobile"],
              "Certifications": ["CISSP", "CISM","CCNA","GISF","CAPM"],
            }
    
    parentList = []
    #Make all the keys in the Dict to lowercase
    catagoriesDict = _lowercase(catagoriesDict)
    #Loop through all skill in the dataframe until it finds the matching skill in dict
    for skills in dataF['Skill']:
        cataFound = False
        #Finding if there is a match to the
        for catagory in catagoriesDict:
            #print(skills)
            if skills in catagoriesDict[catagory]:
                #print(catagory)
                parentList.append(catagory)
                cataFound = True
                break
            else:
                cataFound=False
        #If skill is not in Dict it will be label as Others
        if (not cataFound):
            #print("Not Found")
            parentList.append('Others')
    return parentList