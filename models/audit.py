# models/audit.py
from config.database import get_connection
from datetime import datetime
from decimal import Decimal
import json
class Audit:
    
    @staticmethod
    def log_change(table_name, record_id, action_type, old_values, new_values, admin_id):
        conn = get_connection()
        cursor = conn.cursor()
        

        old_values_json = json.dumps({k: v.isoformat() if isinstance(v, datetime) else str(v) if isinstance(v, Decimal) else v for k, v in old_values.items()}) if old_values else None
        new_values_json = json.dumps({k: v.isoformat() if isinstance(v, datetime) else str(v) if isinstance(v, Decimal) else v for k, v in new_values.items()}) if new_values else None
        

        
        cursor.execute(
            """INSERT INTO audit_log 
            (table_name, record_id, action_type, old_values, new_values, admin_id) 
            VALUES (%s, %s, %s, %s, %s, %s)""",
            (table_name, record_id, action_type, old_values_json, new_values_json, admin_id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def get_audit_logs(filters=None):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
            SELECT al.*, a.username as admin_name
            FROM audit_log al
            JOIN admin a ON al.admin_id = a.id
        """
        
        where_conditions = []
        params = []
        
        if filters:
            if 'id' in filters:
                where_conditions.append("al.id = %s")
                params.append(filters['id'])
            if 'table_name' in filters:
                where_conditions.append("table_name = %s")
                params.append(filters['table_name'])
            if 'action_type' in filters:
                where_conditions.append("action_type = %s")
                params.append(filters['action_type'])
        
        if where_conditions:
            query += " WHERE " + " AND ".join(where_conditions)
        
        query += " ORDER BY timestamp DESC"
        
        cursor.execute(query, tuple(params))
        results = cursor.fetchall()
        
        # Parse JSON strings to dictionaries
        for row in results:
            try:
                if row['old_values'] and isinstance(row['old_values'], str):
                    row['old_values'] = json.loads(row['old_values'])
                if row['new_values'] and isinstance(row['new_values'], str):
                    row['new_values'] = json.loads(row['new_values'])
            except json.JSONDecodeError:
                row['old_values'] = {}
                row['new_values'] = {}
                
        conn.close()
        return results

    @staticmethod
    def get_audit_log_by_id(log_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
            SELECT al.*, a.username as admin_name
            FROM audit_log al
            JOIN admin a ON al.admin_id = a.id
            WHERE al.id = %s
        """
        
        cursor.execute(query, (log_id,))
        result = cursor.fetchone()
        
        if result:
            try:
                if result['old_values'] and isinstance(result['old_values'], str):
                    result['old_values'] = json.loads(result['old_values'])
                if result['new_values'] and isinstance(result['new_values'], str):
                    result['new_values'] = json.loads(result['new_values'])
            except json.JSONDecodeError:
                result['old_values'] = {}
                result['new_values'] = {}
        
        conn.close()
        return result