from bills.models import Bill

def bill_cal(request):
    return render_to_response('bill_list.html')
