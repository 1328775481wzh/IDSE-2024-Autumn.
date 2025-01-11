import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import statistics as st


data = pd.read_csv('400000_samples.csv')

# Part1 - 数据集解释

analysis=data.drop('Country', axis=1)
columns= analysis.columns.tolist()
metrics={}
for i in columns[1:]:
   metrics[i]= [[analysis[i].max(), analysis[i].min()], analysis[i].mean(), st.mode(analysis[i].tolist()), analysis[i].std(), analysis[i].median()]

print(pd.DataFrame(metrics, index=["Range","Mean", "Mode", "Standard Deviation","Median"]))

#Part2 - 可视化分析

#1.患病患者疾病严重程度可视化分析
data0=data.loc[data['Severity_Mild'].isin([1])]
data1=data.loc[data['Severity_Moderate'].isin([1])]
data2=data.loc[data['Severity_Severe'].isin([1])]
c0=data0['Severity_Mild'].count()
c1=data1['Severity_Moderate'].count()
c2=data2['Severity_Severe'].count()
labels = 'Severity_Mild',  'Severity_Moderate', 'Severity_Severe'
sizes = [c0, c1, c2]
explode = (0.1, 0, 0)
plt.pie(sizes,  labels=labels, autopct='%1.1f%%', explode=explode )
plt.title("Pie Chart for visualizing the severity of the patients present in the dataset ")
plt.show()


#2.各年龄类别下受 Covid-19 影响的男性和女性情况可视化分析
polar = data
cols = ['Age_0-9', 'Age_10-19', 'Age_20-24', 'Age_25-59', 'Age_60+', 'Gender_Female', 'Gender_Male']
ages = ['Age_0-9', 'Age_10-19', 'Age_20-24', 'Age_25-59', 'Age_60+']
polar=polar[cols]

men=[]
women=[]

for i in range(len(cols)- 2):
  m =polar.loc[(polar[cols[i]] == 1) & (polar[cols[5]] == 1)]
  men.append(m[cols[i]].count())
  n =polar.loc[(polar[cols[i]] == 1) & (polar[cols[6]] == 1)]
  women.append(n[cols[i]].count()) 

fig, ax = plt.subplots(figsize=(12, 7), subplot_kw=dict(polar=True))
ax.bar(ages, women, label='Women', alpha=0.8)
ax.bar(ages, men, label='Men', alpha=0.8)
ax.tick_params(labelleft='Off', left='Off')
l = ax.legend(loc='upper left')
l.set_bbox_to_anchor((0, 0))
l.set_title("Polar Chart of all Age Categories against Men and Women")

donut_chart = pd.DataFrame(
    {'Age': ages,
     'Men': men,
     'Women': women
    })

fig, ax = plt.subplots(figsize=(15,5))
men = ax.bar(donut_chart.Age, 'Men', data=donut_chart, label='Men %')
women = ax.bar(donut_chart.Age, 'Women', data=donut_chart, label='Women %')
ax.legend()
ax.set_title("Bar Chart for Visualizing the data of Men and Women across all Age Categories")
plt.show()

#3.各属性之间相关性分析
plt.figure(figsize=[30, 10])
sns.heatmap(data.corr(), annot=True, linewidths=1, vmin=-1, cmap="RdBu_r")
plt.title("Correlation Matrix")
plt.show()

#4.各国受 Covid 影响人数可视化分析
fig, axes = plt.subplots(figsize=(12,12))
sns.countplot(y='Country', data=data)
plt.title("Count Plot for Country")
plt.show()

#5.不同国别与发热症状可视化分析
fig, axes = plt.subplots(figsize=(13, 13))
sns.countplot(x='Country', data=data, hue='Fever')
plt.title("Count Plot for Country vs Fever Symptom")
plt.show()

#6.出现症状国家与无症状国家的可视化分析
fig, axes = plt.subplots(figsize=(13, 13))
sns.countplot(x='Country', data=data, hue='None_Experiencing')
plt.title("Count Plot for Country vs None Experiencing Symptom")
plt.show()

#7.症状组合与病情严重程度的关系
data['Fever_Cough'] = data['Fever'] + data['Dry-Cough']
data['Cough_Difficulty'] = data['Dry-Cough'] + data['Difficulty-in-Breathing']
data['Fever_Difficulty'] = data['Fever'] + data['Difficulty-in-Breathing']

def symptom_combination_label(value):
    if value == 0:
        return 'No Symptom'
    elif value == 1:
        return 'One Symptom'
    elif value == 2:
        return 'Both Symptoms'

data['Fever_Cough_Label'] = data['Fever_Cough'].apply(symptom_combination_label)
data['Cough_Difficulty_Label'] = data['Cough_Difficulty'].apply(symptom_combination_label)
data['Fever_Difficulty_Label'] = data['Fever_Difficulty'].apply(symptom_combination_label)

severity_counts_fever_cough = data.groupby(['Fever_Cough_Label', 'Severity_Mild', 'Severity_Moderate', 'Severity_Severe']).size().reset_index(name='Count')
severity_counts_cough_difficulty = data.groupby(['Cough_Difficulty_Label', 'Severity_Mild', 'Severity_Moderate', 'Severity_Severe']).size().reset_index(name='Count')
severity_counts_fever_difficulty = data.groupby(['Fever_Difficulty_Label', 'Severity_Mild', 'Severity_Moderate', 'Severity_Severe']).size().reset_index(name='Count')

# 柱状图展示 Fever + Cough 症状组合与病情严重程度的关系
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='Fever_Cough_Label', y='Count', hue='Severity_Mild', data=severity_counts_fever_cough, ax=ax, palette='Set1')
ax.set_title('Fever + Cough Symptom Combination vs Severity_Mild')
ax.set_xlabel('Fever + Cough Symptom Combination')
ax.set_ylabel('Number of Patients')
plt.show()

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='Fever_Cough_Label', y='Count', hue='Severity_Moderate', data=severity_counts_fever_cough, ax=ax, palette='Set2')
ax.set_title('Fever + Cough Symptom Combination vs Severity_Moderate')
ax.set_xlabel('Fever + Cough Symptom Combination')
ax.set_ylabel('Number of Patients')
plt.show()

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='Fever_Cough_Label', y='Count', hue='Severity_Severe', data=severity_counts_fever_cough, ax=ax, palette='Set3')
ax.set_title('Fever + Cough Symptom Combination vs Severity_Severe')
ax.set_xlabel('Fever + Cough Symptom Combination')
ax.set_ylabel('Number of Patients')
plt.show()

# 柱状图展示 Cough + Difficulty-in-Breathing 症状组合与病情严重程度的关系
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='Cough_Difficulty_Label', y='Count', hue='Severity_Mild', data=severity_counts_cough_difficulty, ax=ax, palette='Set1')
ax.set_title('Cough + Difficulty-in-Breathing Symptom Combination vs Severity_Mild')
ax.set_xlabel('Cough + Difficulty-in-Breathing Symptom Combination')
ax.set_ylabel('Number of Patients')
plt.show()

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='Cough_Difficulty_Label', y='Count', hue='Severity_Moderate', data=severity_counts_cough_difficulty, ax=ax, palette='Set2')
ax.set_title('Cough + Difficulty-in-Breathing Symptom Combination vs Severity_Moderate')
ax.set_xlabel('Cough + Breath Difficulty Symptom Combination')
ax.set_ylabel('Number of Patients')
plt.show()

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='Cough_Difficulty_Label', y='Count', hue='Severity_Severe', data=severity_counts_cough_difficulty, ax=ax, palette='Set3')
ax.set_title('Cough + Difficulty-in-Breathing Symptom Combination vs Severity_Severe')
ax.set_xlabel('Cough + Difficulty-in-Breathing Symptom Combination')
ax.set_ylabel('Number of Patients')
plt.show()

# 柱状图展示 Fever + Difficulty-in-Breathing 症状组合与病情严重程度的关系
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='Fever_Difficulty_Label', y='Count', hue='Severity_Mild', data=severity_counts_fever_difficulty, ax=ax, palette='Set1')
ax.set_title('Fever + Difficulty-in-Breathing Symptom Combination vs Severity_Mild')
ax.set_xlabel('Fever + Difficulty-in-Breathing Symptom Combination')
ax.set_ylabel('Number of Patients')
plt.show()

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='Fever_Difficulty_Label', y='Count', hue='Severity_Moderate', data=severity_counts_fever_difficulty, ax=ax, palette='Set2')
ax.set_title('Fever + Difficulty-in-Breathing Symptom Combination vs Severity_Moderate')
ax.set_xlabel('Fever + Difficulty-in-Breathing Symptom Combination')
ax.set_ylabel('Number of Patients')
plt.show()

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='Fever_Difficulty_Label', y='Count', hue='Severity_Severe', data=severity_counts_fever_difficulty, ax=ax, palette='Set3')
ax.set_title('Fever + Difficulty-in-Breathing Symptom Combination vs Severity_Severe')
ax.set_xlabel('Fever + Difficulty-in-Breathing Symptom Combination')
ax.set_ylabel('Number of Patients')
plt.show()

# 热力图展示症状组合与病情严重程度的关系
pivot_fever_cough = severity_counts_fever_cough.pivot_table(index='Fever_Cough_Label', columns='Severity_Mild', values='Count', fill_value=0)
pivot_cough_difficulty = severity_counts_cough_difficulty.pivot_table(index='Cough_Difficulty_Label', columns='Severity_Moderate', values='Count', fill_value=0)
pivot_fever_difficulty = severity_counts_fever_difficulty.pivot_table(index='Fever_Difficulty_Label', columns='Severity_Severe', values='Count', fill_value=0)

fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(pivot_fever_cough, annot=True, cmap='YlGnBu', ax=ax)
ax.set_title('Heatmap of Fever + Cough vs Severity_Mild')
plt.show()

fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(pivot_cough_difficulty, annot=True, cmap='YlGnBu', ax=ax)
ax.set_title('Heatmap of Cough + Difficulty-in-Breathing vs Severity_Moderate')
plt.show()

fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(pivot_fever_difficulty, annot=True, cmap='YlGnBu', ax=ax)
ax.set_title('Heatmap of Fever + Difficulty-in-Breathing vs Severity_Severe')
plt.show()