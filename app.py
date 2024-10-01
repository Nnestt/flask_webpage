from flask import Flask, render_template
import plotly.express as px
import plotly.io as pio
import pandas as pd

app = Flask(__name__)

df = pd.read_csv('data\\USprocessed.csv')
df2 = pd.read_csv('data\\SGprocessed.csv')

# Sample function to create a Plotly graph
def create_plotly_graph():
    # Create a simple scatter plot using Plotly
    ex = px.data.iris()  # Example dataset
    fig = px.scatter(ex, x="sepal_width", y="sepal_length", color="species", title="Iris Dataset Scatter Plot")
    
    # Convert the Plotly figure to an HTML div string
    graph_html = pio.to_html(fig, full_html=False)
    return graph_html


# MOST SEEKED JOBS IN US

def most_seeked_us():
  job_counts = df['jobtitle'].value_counts().reset_index()
  job_counts.columns = ['jobtitle', 'jobNo']
  # # Debugging: Print the job_counts DataFrame to check its contents
  # print(job_counts.head(20))

  # # Ensure jobNo is of numeric type
  # job_counts['jobNo'] = pd.to_numeric(job_counts['jobNo'], errors='coerce')

  # Create a horizontal bar chart
  fig = px.bar(job_counts.head(20),
        y='jobtitle',
        x='jobNo',
        title="Most seeked Jobs (US)",
        labels={'jobNo': 'Number of Job Postings', 'jobtitle': 'Job Title'},
        color='jobtitle',
        orientation='h')

  # Update layout for font size and y-axis limits
  fig.update_layout(
    yaxis=dict(title='Job Title', tickfont_size=10,),
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
  fig = px.bar(job_counts.head(20),
        y='jobtitle',
        x='jobNo',
        title="Most seeked Jobs (Singapore)",
        labels={'jobNo': 'Number of Job Postings', 'jobtitle': 'Job Title'},
        color='jobtitle',
        orientation='h')

  # Update layout for font size and y-axis limits
  fig.update_layout(
    yaxis=dict(title='Job Title', tickfont_size=10,),
    xaxis=dict(title='Number of Job Postings', tickfont_size=14),
    title=dict(font=dict(size=16)),
    yaxis_range=[-0.5, 20.5],  # Adjust range to fit the plot
  )

  # Convert the Plotly figure to an HTML div string
  ms_sg_html = pio.to_html(fig, full_html=False)
  return ms_sg_html

# END MOST SEEKED JOBS IN SG
# =================================================================================================



# ROUTES
# =================================================================================================
# Homepage route
@app.route('/')
def home():
    graph_html = create_plotly_graph()
    ms_us_html = most_seeked_us()
    ms_sg_html = most_seeked_sg()
    return render_template('index.html', graph_html=graph_html, ms_us_html=ms_us_html, ms_sg_html=ms_sg_html)

# @app.route('/sg')
# def about():
#     return render_template('sg.html')

# @app.route('/us')
# def about():
#     return render_template('us.html')

if __name__ == '__main__':
    app.run(debug=True)

