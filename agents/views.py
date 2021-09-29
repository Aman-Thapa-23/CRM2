from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import reverse
from leads.models import Agent
from .forms import AgentModelForm


class AgentListView(LoginRequiredMixin, generic.ListView):
    template_name="agents/agent_list.html"
    queryset= Agent.objects.all()
    context_object_name = "agents"


class AgentCreateView(LoginRequiredMixin, generic.CreateView):
    template_name="agents/agent_create.html"
    form_class= AgentModelForm

    def get_success_url(self):
        return reverse("agent_List")

    def form_valid(self, form):
        agent=form.save(commit=False)
        agent.organization =self.request.user.userprofile
        agent.save()
        return super(AgentCreateView, self).form_valid(form)


class AgentDetailView(LoginRequiredMixin, generic.DetailView):
    template_name="agents/agent_details.html"