from django.core.mail import send_mail
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView, DetailView , CreateView, UpdateView ,DeleteView
#or from django.views import generic
from . models import Lead
from .forms import LeadForm, CustomeUserCreationForm

#view of authentication
class SignUpView(CreateView):
    template_name = "registration/signup.html"
    form_class = CustomeUserCreationForm

    def get_success_url(self):
        return reverse('login')


# class view of Lead
class LandingPageView(TemplateView):    
    template_name = "landing.html"

class LeadListView(LoginRequiredMixin, ListView):
    template_name = "leads/lead_list.html"
    queryset = Lead.objects.all()
    context_object_name = "leads"

class LeadDetailsView(LoginRequiredMixin, DetailView):
    template_name = "leads/lead_details.html"
    queryset = Lead.objects.all()
    context_object_name = "lead"

class LeadCreateView(LoginRequiredMixin, CreateView):
    template_name = "leads/lead_create.html"
    form_class = LeadForm

    def get_success_url(self):
        return reverse('lead_list')

    def form_valid(self, form):
        send_mail(
            subject="A lead has been created",
            message="Go to the site to see new lead",
            from_email="test@test.com",
            recipient_list=["test2@test.com"]
        )
        return super(LeadCreateView, self).form_valid(form) 

class LeadUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "leads/lead_update.html"
    queryset = Lead.objects.all()
    form_class = LeadForm

    def get_success_url(self):
        return reverse('lead_list')

class LeadDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "leads/lead_delete.html"
    queryset = Lead.objects.all()

    def get_success_url(self):
        return reverse('lead_list')


#     function view
def landing_page(request):
    return render(request, "landing.html")

def lead_list(request):
    leads = Lead.objects.all()
    context ={"leads": leads}
    return render(request, "leads/lead_list.html", context)


def lead_details(request, pk):
    lead = Lead.objects.get(id=pk)
    context ={"lead": lead}
    return render(request, "leads/lead_details.html", context)

def lead_create(request):
    form = LeadForm()
    if request.method == "POST":
        form = LeadForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lead_list')
    context={ "form":form }
    return render(request, 'leads/lead_create.html', context)

def lead_update(request, pk):
    lead =Lead.objects.get(id=pk)
    form = LeadForm(instance=lead)
    if request.method == "POST":
        form = LeadForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            return redirect('lead_list')
    context= {
        'form': form,
        'lead': lead
        }
    return render(request, 'leads/lead_update.html', context)

def lead_delete(request, pk):
    lead = Lead.objects.get(id=pk)
    lead.delete()
    return redirect("/leads")
    