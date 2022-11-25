# Import module
import sqlite3
import pandas as pd

df_job = pd.DataFrame({
    "user_id": [1, 2, 3, 4],
    "job": ["Data Science", "Python programmer",
    "ML engineer", "Java programmer"]
})
con = sqlite3.connect("test.db")
df_job.to_sql("Job", con)