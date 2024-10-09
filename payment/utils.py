from datetime import datetime

def generate_receipt_id(Receipt):
    latest_transaction = Receipt.objects.filter(
        created_at__year=datetime.now().year
    ).order_by('id').last()
    
    if not latest_transaction:
        return f"GREEN-REC-{datetime.now().year}{datetime.now().month}{datetime.now().day}{datetime.now().hour}{datetime.now().minute}-0001"
    
    receipt_id = int(latest_transaction.receipt_id.split('-')[-1]) + 1
    return f"GREEN-REC-{datetime.now().year}{datetime.now().month}{datetime.now().day}{datetime.now().hour}{datetime.now().minute}-{receipt_id:04d}"


def generate_refund_id(Refund):
    latest_transaction = Refund.objects.filter(
        created_at__year=datetime.now().year
    ).order_by('id').last()
    
    if not latest_transaction:
        return f"GREEN-RFD-{datetime.now().year}{datetime.now().month}{datetime.now().day}{datetime.now().hour}{datetime.now().minute}-0001"
    
    refund_id = int(latest_transaction.refund_id.split('-')[-1]) + 1
    return f"GREEN-RFD-{datetime.now().year}{datetime.now().month}{datetime.now().day}{datetime.now().hour}{datetime.now().minute}-{refund_id:04d}"