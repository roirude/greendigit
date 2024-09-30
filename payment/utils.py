from datetime import datetime

def generate_receipt_id(Receipt):
    latest_transaction = Receipt.objects.filter(
        created_at__year=datetime.now().year
    ).order_by('id').last()
    
    if not latest_transaction:
        return f"REC-{datetime.now().year}-0001"
    
    receipt_id = int(latest_transaction.receipt_id.split('-')[-1]) + 1
    return f"REC-{datetime.now().year}-{receipt_id:04d}"