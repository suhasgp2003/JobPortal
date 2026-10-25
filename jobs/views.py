from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import JobForm, ApplicationForm
from .models import Job, Application


def job_list(request):
    jobs = Job.objects.all()
    return render(request, 'jobs/job_list.html', {'jobs': jobs})


def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    return render(request, 'jobs/detail.html', {'job': job})


@login_required
def create_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.owner = request.user
            job.save()
            return redirect('my_jobs')
    else:
        form = JobForm()

    return render(request, 'jobs/create_job.html', {'form': form})


@login_required
def my_jobs(request):
    jobs = Job.objects.filter(owner=request.user)
    return render(request, 'jobs/my_jobs.html', {'jobs': jobs})


@login_required
def edit_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, owner=request.user)

    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('my_jobs')
    else:
        form = JobForm(instance=job)

    return render(request, 'jobs/edit_job.html', {'form': form})


@login_required
def delete_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, owner=request.user)
    job.delete()
    return redirect('my_jobs')


@login_required
def apply_to_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.save()
            return redirect('job_detail', job_id=job.id)
    else:
        form = ApplicationForm()

    return render(request, 'jobs/apply.html', {'form': form, 'job': job})


@login_required
def view_applications(request, job_id):
    job = get_object_or_404(Job, id=job_id, owner=request.user)
    applications = Application.objects.filter(job=job)

    return render(request, 'jobs/applications.html', {
        'job': job,
        'applications': applications
    })
