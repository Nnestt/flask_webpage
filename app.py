from flask import Flask, render_template
import plotly.express as px
import plotly.io as pio
import pandas as pd
from functions import explodeSkill, explodeSkillCata, getTopXSkill, catagoriseSkills, category_colors

app = Flask(__name__)

# PREPROCESSED DATA
df = pd.read_csv('data\\processed_us.csv')
df2 = pd.read_csv('data\\processed_sg.csv')
# FOR SKILLS PORTION
df_exploded = explodeSkill(df)
top_20_skills_us = getTopXSkill(df_exploded,20)
df2_exploded = explodeSkill(df2)
top_20_skills_sg = getTopXSkill(df2_exploded,20)

# GRAPHS =================================================================================================

# COMPANIES WITH MOST JOB POSTINGS IN US

def most_job_us():
  company_counts = df['company'].value_counts().reset_index()
  company_counts.columns = ['company', 'job_postings']

  # Truncate comapny titles that are too long
  max_title_length = 20
  company_counts['company'] = company_counts['company'].apply(
    lambda x: (x[:max_title_length] + '...') if len(x) > max_title_length else x)

  # Create a horizontal bar chart
  fig = px.bar(company_counts,
        y='company',
        x='job_postings',
        title="Companies with Most Job Postings (US)",
        labels={'job_postings': 'Number of Job Postings', 'company': 'Company Name'},
        color='job_postings',
        orientation='h')

  # Update layout for font size and y-axis limits
  fig.update_layout(
    yaxis=dict(title='Company Name', tickfont_size=14,),
    xaxis=dict(title='Number of Job Postings', tickfont_size=14),
    title=dict(font=dict(size=18)),
    yaxis_range=[10.5, -0.5]  # Adjust range to fit the plot
  )

  # Convert the Plotly figure to a HTML div string
  c_us_html = pio.to_html(fig, full_html=False)
  return c_us_html

# =================================================================================================

# COMPANIES WITH MOST JOB POSTINGS IN SG
def most_job_sg():
  company_counts = df2['Company Name'].value_counts().reset_index()
  company_counts.columns = ['company', 'job_postings']

  # Truncate comapny titles that are too long
  max_title_length = 20
  company_counts['company'] = company_counts['company'].apply(lambda x: (x[:max_title_length] + '...') if len(x) > max_title_length else x)


  # Create a horizontal bar chart
  fig = px.bar(company_counts,
        y='company',
        x='job_postings',
        title="Companies with Most Job Postings (Singapore)",
        labels={'job_postings': 'Number of Job Postings', 'company': 'Company Name'},
        color='job_postings',
        orientation='h')

  # Update layout for font size and y-axis limits
  fig.update_layout(
    yaxis=dict(title='Company Name', tickfont_size=14,),
    xaxis=dict(title='Number of Job Postings', tickfont_size=14),
    title=dict(font=dict(size=18)),
    yaxis_range=[10.5, -0.5]  # Adjust range to fit the plot
  )

  # Convert the Plotly figure to an HTML div string
  c_sg_html = pio.to_html(fig, full_html=False)
  return c_sg_html

# =================================================================================================

# MOST SEEKED JOBS IN US

def most_seeked_us():
  job_counts = df['jobtitle'].value_counts().reset_index()
  job_counts.columns = ['jobtitle', 'jobNo']
  # # Debugging: Print the job_counts DataFrame to check its contents
  # print(job_counts.head(20))

  # # Ensure jobNo is of numeric type
  # job_counts['jobNo'] = pd.to_numeric(job_counts['jobNo'], errors='coerce')

    # Truncate job titles that are too long
  max_title_length = 20
  job_counts['jobtitle'] = job_counts['jobtitle'].apply(lambda x: (x[:max_title_length] + '...') if len(x) > max_title_length else x)


  # Create a horizontal bar chart
  fig = px.bar(job_counts.head(21),
        y='jobtitle',
        x='jobNo',
        title="Most seeked Jobs (US)",
        labels={'jobNo': 'Number of Job Postings', 'jobtitle': 'Job Title'},
        color='jobtitle',
        orientation='h')

  # Update layout for font size and y-axis limits
  fig.update_layout(
    yaxis=dict(title='Job Title', tickfont_size=14,),
    xaxis=dict(title='Number of Job Postings', tickfont_size=14),
    title=dict(font=dict(size=16)),
    yaxis_range=[-0.5, 20.5],  # Adjust range to fit the plot
  )

  # Convert the Plotly figure to an HTML div string
  ms_us_html = pio.to_html(fig, full_html=False)
  return ms_us_html

# END MOST SEEKED JOBS IN US 
# =================================================================================================


# MOST SEEKED JOBS IN SG
def most_seeked_sg():
  job_counts = df2['Job Title'].value_counts().reset_index()
  job_counts.columns = ['jobtitle', 'jobNo']

  # Truncate job titles that are too long
  max_title_length = 20
  job_counts['jobtitle'] = job_counts['jobtitle'].apply(lambda x: (x[:max_title_length] + '...') if len(x) > max_title_length else x)

  # Create a horizontal bar chart
  fig = px.bar(job_counts.head(21), #20 doesnt show rank 1
        y='jobtitle',
        x='jobNo',
        title="Most seeked Jobs (Singapore)",
        labels={'jobNo': 'Number of Job Postings', 'jobtitle': 'Job Title'},
        color='jobtitle',
        orientation='h')

  # Update layout for font size and y-axis limits
  fig.update_layout(
    yaxis=dict(title='Job Title', tickfont_size=14,),
    xaxis=dict(title='Number of Job Postings', tickfont_size=14),
    title=dict(font=dict(size=16)),
    yaxis_range=[-0.5, 20.5],  # Adjust range to fit the plot
  )

  # Convert the Plotly figure to an HTML div string
  ms_sg_html = pio.to_html(fig, full_html=False)
  return ms_sg_html

# END MOST SEEKED JOBS IN SG
# =================================================================================================

# SKILLS IN DEMAND

# SG SKILLS ==========================================================================================


def sg_top_skills(top_20_skills_sg):
    fig = px.bar(top_20_skills_sg,
                  x='Skill',
                  y='Count',
                  title='Top 20 Skills (Singapore)',
                  color='Skill')

    fig.update_layout(
        yaxis=dict(title='Skill', tickfont_size=14),
        xaxis=dict(title='Count', tickfont_size=14),
        title=dict(font=dict(size=18)),
    )
    sg_skills_html = pio.to_html(fig, full_html=False)
    return sg_skills_html

def sg_top_skills_cat(top_20_skills_sg):
    top_20_skills_sg['catagory'] = catagoriseSkills(top_20_skills_sg)
    fig = px.sunburst(top_20_skills_sg, path=['catagory', 'Skill'], 
                  values='Count',title='Most Sought after Skills (Singapore)', color='catagory',
                  color_discrete_map=category_colors)
    fig.update_layout(
    margin = dict(t=80, l=10, r=10, b=10),
    )
    sg_skills_html_cat = pio.to_html(fig, full_html=False)
    return sg_skills_html_cat


def sg_se_skills():
  tempDF = explodeSkillCata(df2, 'Software Engineering')
  dfTop20 = getTopXSkill(tempDF, 20)

  dfTop20['catagory'] = catagoriseSkills(dfTop20)
  fig = px.sunburst(dfTop20, path=['catagory', 'Skill'], 
            values='Count', title='Top Categories Software Engineering (Singapore)', color='catagory',
            color_discrete_map=category_colors)
  fig.update_layout(
  margin = dict(t=80, l=10, r=10, b=10),
  )
  sg_se_skills_html = pio.to_html(fig, full_html=False)
  return sg_se_skills_html

def sg_is_skills():
  # Cyber (SG)
  tempDF = explodeSkillCata(df2, 'Cybersecurity')
  dfTop20 = getTopXSkill(tempDF, 20)

  dfTop20['catagory'] = catagoriseSkills(dfTop20)
  fig = px.sunburst(dfTop20, path=['catagory', 'Skill'], 
            values='Count', title='Top Categories Cybersecurity (Singapore)', color='catagory',
            color_discrete_map=category_colors)
  fig.update_layout(
  margin = dict(t=80, l=10, r=10, b=10),
  )
  sg_is_skills_html = pio.to_html(fig, full_html=False)
  return sg_is_skills_html

# SG SKILLS END ==========================================================================================

# US SKILLS ==========================================================================================

def us_top_skills(top_20_skills_us):
  fig = px.bar(top_20_skills_us,
                x='Skill',
                y='Count',
                title='Top 20 Skills (US)',
                color='Skill',)

  fig.update_layout(
      yaxis=dict(title='Skill', tickfont_size=14,),
      xaxis=dict(title='Count', tickfont_size=14),
      title=dict(font=dict(size=18)),
  )
  us_skills_html = pio.to_html(fig, full_html=False)
  return us_skills_html

def us_top_skills_cat(top_20_skills_us):
    top_20_skills_us['catagory'] = catagoriseSkills(top_20_skills_us)
    fig = px.sunburst(top_20_skills_us, path=['catagory', 'Skill'], 
                      values='Count', title='Most Sought After Skills (US)', color='catagory',
                      color_discrete_map=category_colors)
    fig.update_layout(
    margin = dict(t=80, l=10, r=10, b=10),
    )
    us_skills_html_cat = pio.to_html(fig, full_html=False)
    return us_skills_html_cat

def us_se_skills():
  # Developer (dice)
  tempDF = explodeSkillCata(df, 'Software Engineering')
  dfTop20 = getTopXSkill(tempDF, 20)

  dfTop20['catagory'] = catagoriseSkills(dfTop20)
  fig = px.sunburst(dfTop20, path=['catagory', 'Skill'], 
            values='Count', title='Top Categories Software Engineering (US)', color='catagory',
            color_discrete_map=category_colors)
  fig.update_layout(
  margin = dict(t=80, l=10, r=10, b=10),
  )
  us_se_skills_html = pio.to_html(fig, full_html=False)
  return us_se_skills_html


def us_is_skills():
  # Cyber (dice)
  tempDF = explodeSkillCata(df, 'Cybersecurity')
  dfTop20 = getTopXSkill(tempDF, 20)

  dfTop20['catagory'] = catagoriseSkills(dfTop20)
  fig = px.sunburst(dfTop20, path=['catagory', 'Skill'], 
            values='Count', title='Top Categories Cybersecurity (US)', color='catagory',
            color_discrete_map=category_colors)
  fig.update_layout(
  margin = dict(t=80, l=10, r=10, b=10),
  )
  us_is_skills_html = pio.to_html(fig, full_html=False)
  return us_is_skills_html

# US SKILLS END  ==========================================================================================


# GRAPHS END ==========================================================================================

# ROUTES
# =================================================================================================
# Homepage route
@app.route('/')
def home():
    ms_us_html = most_seeked_us()
    ms_sg_html = most_seeked_sg()
    c_us_html = most_job_us()
    c_sg_html = most_job_sg()
    sg_top_skills_html = sg_top_skills(top_20_skills_sg)
    us_top_skills_html = us_top_skills(top_20_skills_us)
    sg_top_skills_cat_html = sg_top_skills_cat(top_20_skills_sg)
    us_top_skills_cat_html = us_top_skills_cat(top_20_skills_us)
    sg_se_skills_html = sg_se_skills()
    sg_is_skills_html = sg_is_skills()
    us_se_skills_html = us_se_skills()
    us_is_skills_html = us_is_skills()
    return render_template('index.html', 
                          ms_us_html=ms_us_html, 
                          ms_sg_html=ms_sg_html, 
                          c_us_html=c_us_html, 
                          c_sg_html=c_sg_html,
                          sg_top_skills_html=sg_top_skills_html,
                          us_top_skills_html=us_top_skills_html,
                          sg_top_skills_cat_html= sg_top_skills_cat_html,
                          us_top_skills_cat_html= us_top_skills_cat_html,
                          sg_se_skills_html=sg_se_skills_html,
                          sg_is_skills_html=sg_is_skills_html,
                          us_se_skills_html=us_se_skills_html,
                          us_is_skills_html=us_is_skills_html
                          
                          )

# @app.route('/sg')
# def about():
#     return render_template('sg.html')

# @app.route('/us')
# def about():
#     return render_template('us.html')

if __name__ == '__main__':
    app.run(debug=True)

