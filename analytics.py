# ============================================================
# ANALYTICS MODULE — Pandas & NumPy
# Smart Task Management System
# ============================================================

import sqlite3
import pandas as pd
import numpy as np

def get_analytics(user_id, db_name='tasks.db'):
    try:
        conn = sqlite3.connect(db_name)

        # Load tasks into Pandas DataFrame
        df = pd.read_sql_query(
            'SELECT * FROM tasks WHERE user_id = ?',
            conn,
            params=(user_id,)
        )
        conn.close()

        if df.empty:
            return {
                'total_tasks': 0,
                'completed_tasks': 0,
                'pending_tasks': 0,
                'in_progress_tasks': 0,
                'completion_percentage': 0.0,
                'priority_breakdown': {},
                'status_breakdown': {},
                'average_tasks_per_day': 0.0
            }

        # Basic analytics using Pandas
        total_tasks      = len(df)
        completed_tasks  = len(df[df['status'] == 'Completed'])
        pending_tasks    = len(df[df['status'] == 'Pending'])
        in_progress      = len(df[df['status'] == 'In Progress'])

        # Completion percentage using NumPy
        completion_pct = np.round((completed_tasks / total_tasks) * 100, 2) if total_tasks > 0 else 0.0

        # Priority breakdown
        priority_counts = df['priority'].value_counts().to_dict()

        # Status breakdown
        status_counts = df['status'].value_counts().to_dict()

        # Tasks per day using Pandas datetime
        df['created_at'] = pd.to_datetime(df['created_at'])
        df['date']       = df['created_at'].dt.date
        tasks_per_day    = df.groupby('date').size()
        avg_per_day      = np.round(tasks_per_day.mean(), 2) if len(tasks_per_day) > 0 else 0.0

        return {
            'total_tasks':          int(total_tasks),
            'completed_tasks':      int(completed_tasks),
            'pending_tasks':        int(pending_tasks),
            'in_progress_tasks':    int(in_progress),
            'completion_percentage': float(completion_pct),
            'priority_breakdown':   priority_counts,
            'status_breakdown':     status_counts,
            'average_tasks_per_day': float(avg_per_day)
        }

    except Exception as e:
        return {'error': str(e)}
