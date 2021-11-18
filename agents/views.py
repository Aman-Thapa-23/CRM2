from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import reverse
from leads.models import Agent
from .forms import AgentModelForm
from .mixins import OrganizerAndLoginRequiredMixin


class AgentListView(OrganizerAndLoginRequiredMixin, generic.ListView):
    template_name="agents/agent_list.html"
    context_object_name = "agents"
    
    def get_queryset(self):
        organization = self.request.user.userprofile
        return Agent.objects.filter(organization=organization)
    


class AgentCreateView(OrganizerAndLoginRequiredMixin, generic.CreateView):
    template_name="agents/agent_create.html"
    form_class= AgentModelForm

    def get_success_url(self):
        return reverse("agent_list")

    def form_valid(self, form):
        user=form.save(commit=False)
        user.is_agent = True
        user.is_organizer = False
        user.save()
        Agent.objects.create(
            user=user,
            organization =self.request.user.userprofile

        )
        send_mail(
            subject="You are invited to be an agent",
            message="You were added as an agent on DJCRM. Please come login to start working.",
            from_email = "admin@gmail.com",
            receipent_list=[user.email]
        )
        return super(AgentCreateView, self).form_valid(form)


class AgentDetailView(OrganizerAndLoginRequiredMixin, generic.DetailView):
    template_name="agents/agent_details.html"
    queryset = Agent.objects.all()
    context_object_name = "agent"



class AgentUpdateView(OrganizerAndLoginRequiredMixin, generic.UpdateView):
    template_name="agents/agent_update.html"
    form_class= AgentModelForm
    queryset = Agent.objects.all()

    def get_success_url(self):
        return reverse("agent_list")


class AgentDeleteView(OrganizerAndLoginRequiredMixin, generic.DeleteView):
    template_name = "agents/agent_delete.html"
    queryset = Agent.objects.all()
    context_object_name = "agent"

    def get_success_url(self):
        return reverse("agent_list")