from django.core.mail import send_mail
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView, DetailView , CreateView, UpdateView ,DeleteView
from django.views.generic.edit import FormView
#or from django.views import generic
from . models import Lead
from .forms import LeadForm, CustomeUserCreationForm, AssignAgentForm
from agents.mixins import OrganizerAndLoginRequiredMixin

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
    context_object_name = "leads"

    def get_queryset(self):
        user = self.request.user

        # initial queryset of leads for the entire organzation
        if user.is_organizer:
            queryset = Lead.objects.filter(
                organization=user.userprofile,
                agent__isnull=False
            )
        else:
            queryset=Lead.objects.filter(organization=user.agent.organization, agent__isnull=False)
            # filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(LeadListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organizer:
            queryset = Lead.objects.filter(
                organization=user.userprofile,
                agent__isnull=True
            )
        context.update({
            "unassigned_leads": queryset
        })
        
        return context        

class LeadDetailsView(LoginRequiredMixin, DetailView):
    template_name = "leads/lead_details.html"
    context_object_name = "lead"
    def get_queryset(self):
        user = self.request.user

        # initial queryset of leads for the entire organzation
        if user.is_organizer:
            queryset = Lead.objects.filter(organization=user.userprofile)
        else:
            queryset=Lead.objects.filter(organization=user.agent.organization)
            # filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
        return queryset

class LeadCreateView(OrganizerAndLoginRequiredMixin, CreateView):
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

class LeadUpdateView(OrganizerAndLoginRequiredMixin, UpdateView):
    template_name = "leads/lead_update.html"
    form_class = LeadForm
    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organzation
        return Lead.objects.filter(organization=user.userprofile)

    def get_success_url(self):
        return reverse('lead_list')

class LeadDeleteView(OrganizerAndLoginRequiredMixin, DeleteView):
    template_name = "leads/lead_delete.html"
    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organzation
        return Lead.objects.filter(organization=user.userprofile)

    def get_success_url(self):
        return reverse('lead_list')

class AssignAgentView(OrganizerAndLoginRequiredMixin, FormView):
    template_name="leads/assign_agent.html"
    form_class= AssignAgentForm

    def get_form_kwargs(self):
        return {
            "request": self.request
        }

    def get_success_url(self):
        return reverse('lead_list')



#     function view
# def landing_page(request):
#     return render(request, "landing.html")

# def lead_list(request):
#     leads = Lead.objects.all()
#     context ={"leads": leads}
#     return render(request, "leads/lead_list.html", context)


# def lead_details(request, pk):
#     lead = Lead.objects.get(id=pk)
#     context ={"lead": lead}
#     return render(request, "leads/lead_details.html", context)

# def lead_create(request):
#     form = LeadForm()
#     if request.method == "POST":
#         form = LeadForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('lead_list')
#     context={ "form":form }
#     return render(request, 'leads/lead_create.html', context)

# def lead_update(request, pk):
#     lead =Lead.objects.get(id=pk)
#     form = LeadForm(instance=lead)
#     if request.method == "POST":
#         form = LeadForm(request.POST, instance=lead)
#         if form.is_valid():
#             form.save()
#             return redirect('lead_list')
#     context= {
#         'form': form,
#         'lead': lead
#         }
#     return render(request, 'leads/lead_update.html', context)

# def lead_delete(request, pk):
#     lead = Lead.objects.get(id=pk)
#     lead.delete()
#     return redirect("/leads")
    