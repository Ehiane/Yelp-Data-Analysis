import json
import csv
import psycopg2
import pandas as pd

def create_csv_from_json(json_file, csv_file, fields, integer_fields=None):
    if integer_fields is None:
        integer_fields = []
    with open(json_file, 'r', encoding='utf-8') as infile, open(csv_file, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(fields)  # Write header
        for line in infile:
            data = json.loads(line)
            row = []
            for field in fields:
                if field in integer_fields:
                    row.append(data.get(field, 0))  # Use 0 for missing integer values
                else:
                    row.append(data.get(field, 'UNKNOWN'))  # Use 'UNKNOWN' for other missing values
            writer.writerow(row)

def connect():
    conn = psycopg2.connect(
        dbname="milestone1db",
        user="postgres",
        password="12345",
        host="127.0.0.1",
        port="5432"
    )
    return conn

def import_csv_to_postgres(file_path, table_name, columns, conflict_columns):
    conn = connect()
    cur = conn.cursor()
    
    # Read the CSV file with headers
    df = pd.read_csv(file_path, encoding='utf-8')
    
    for index, row in df.iterrows():
        try:
            # Replace NaN values in integer fields with 0
            for col in columns:
                if col in conflict_columns:
                    continue
                if pd.isna(row[col]) and col in integer_fields:
                    row[col] = 0
                elif pd.isna(row[col]):
                    row[col] = 'UNKNOWN'
            cur.execute(
                f"""
                INSERT INTO {table_name} ({', '.join(columns)}) 
                VALUES ({', '.join(['%s'] * len(columns))}) 
                ON CONFLICT ({', '.join(conflict_columns)}) 
                DO UPDATE SET 
                {', '.join([f"{col} = EXCLUDED.{col}" for col in columns if col not in conflict_columns])}
                """,
                tuple(row)
            )
            print(f"Inserted/Updated row {index} into {table_name}: {row}")
        except Exception as e:
            print(f"Error inserting/updating row {index} into {table_name}: {row}. Error: {e}")
            conn.rollback()  # Rollback the transaction on error
            continue  # Continue with the next row
    
    conn.commit()  # Commit the transaction
    cur.close()
    conn.close()

if __name__ == "__main__":
    # Define file paths and table fields
    user_json_file = 'yelp_user.JSON'
    review_json_file = 'yelp_review.JSON'
    checkin_json_file = 'yelp_checkin.JSON'
    business_json_file = 'yelp_business.JSON'

    user_csv_file = 'yelp_user.csv'
    review_csv_file = 'yelp_review.csv'
    checkin_csv_file = 'yelp_checkin.csv'
    business_csv_file = 'yelp_business.csv'

    user_fields = ['user_id', 'name', 'review_count']
    review_fields = ['review_id', 'user_id', 'business_id', 'stars', 'date']
    checkin_fields = ['business_id', 'day', 'hour', 'checkins']
    business_fields = ['business_id', 'name_', 'state_', 'city']  # Ensure this matches the actual column names

    integer_fields = ['checkins']  # Define integer fields

    # Create CSV files from JSON
    create_csv_from_json(user_json_file, user_csv_file, user_fields)
    create_csv_from_json(review_json_file, review_csv_file, review_fields)
    create_csv_from_json(checkin_json_file, checkin_csv_file, checkin_fields, integer_fields)
    create_csv_from_json(business_json_file, business_csv_file, business_fields)

    # Import CSV data into PostgreSQL
    # import_csv_to_postgres(business_csv_file, 'business', business_fields, ['business_id'])  # Import business data first
    # import_csv_to_postgres(user_csv_file, 'user_', user_fields, ['user_id'])
    # import_csv_to_postgres(review_csv_file, 'review', review_fields, ['review_id'])
    import_csv_to_postgres(checkin_csv_file, 'checkin', checkin_fields, ['business_id', 'day', 'hour'])  # Use composite key for conflict detection
