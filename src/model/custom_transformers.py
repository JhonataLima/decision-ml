def label_encode_df(df):
    import pandas as pd
    from sklearn.preprocessing import LabelEncoder
    df = df.copy()
    cat_cols = df.select_dtypes(include='object').columns.tolist()
    for col in cat_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))
    return df