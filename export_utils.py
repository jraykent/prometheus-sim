import pandas as pd

def export_persona_logs(personas, format="csv"):
    all_logs = []
    for p in personas:
        df = p.export_log()
        df['persona'] = p.name
        all_logs.append(df)
    logs_df = pd.concat(all_logs)
    if format == "csv":
        return logs_df.to_csv(index=False)
    elif format == "json":
        return logs_df.to_json(orient="records")
    return None
