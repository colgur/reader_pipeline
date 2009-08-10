from django.shortcuts import render_to_response, get_object_or_404
from visualizations.labelcloud.models import User

def index(request):
   u = User.objects.get(pk=1)
   feedterm_list = u.label_set.all()
   feedterm_list_length = len(feedterm_list)

   t = 'labelcloud/index.html'
   c = {'feedterm_list': feedterm_list,
        'feedterm_list_length' : feedterm_list_length}
   return render_to_response(t, c)
