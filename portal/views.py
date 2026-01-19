from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Request
from .forms import RequestForm
from django.shortcuts import get_object_or_404
from django.contrib import messages

# Create your views here.

@login_required
def dashboard_view(request):
    from .models import EmployeeProfile
    profile, created = EmployeeProfile.objects.get_or_create(user=request.user)

    if profile.role == 'MANAGER':
        user_requests = Request.objects.all()
    else:
        user_requests = Request.objects.filter(employee=request.user)

    context = {
        'requests': user_requests,
        'role': profile.role,
        'username': request.user.username,
    }
    return render(request, 'portal/dashboard.html', context)

@login_required
def create_request_view(request):
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            new_request = form.save(commit=False)
            new_request.employee = request.user
            new_request.save()

            messages.success(request, 'Your request has been submitted successfully!')
            return redirect('user-home')
    else:
        form = RequestForm()

    return render(request, 'portal/create_request.html', {'form': form})

@login_required
def update_status_view(request, pk, new_status):

    profile = request.user.employeeprofile
    if profile.role != 'MANAGER':
        return redirect('user-home')
    
    req = get_object_or_404(Request, pk=pk)

    req.status = new_status
    req.save()

    return redirect('user-home')

@login_required
def delete_request_view(request, pk):
    req = get_object_or_404(Request, pk=pk, employee=request.user)

    if req.status == 'PENDING':
        req.delete()
        messages.warning(request, 'Request has been canceled and deleted.')
    else:
        messages.error(request, 'You cannot delete a request that has already been processed.')
    
    return redirect('user-home')

@login_required
def request_details_view(request, pk):
    req = get_object_or_404(Request, pk=pk)
    

    context = {
        'req': req,
        'profile': req.employee.employeeprofile,
        'category': req.category,
    }

    return render(request, 'portal/request_details.html', context)