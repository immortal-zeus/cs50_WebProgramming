from django.shortcuts import render
from markdown2 import Markdown
from django.urls import reverse
from django.http import HttpResponseRedirect
from django import forms
from . import util

class Newformnewpage(forms.Form):
    editform = forms.BooleanField(initial=False,widget=forms.HiddenInput(),required=False)
    title = forms.CharField(label="Entry",widget=forms.TextInput(attrs={'class' : 'form-control col-md-6'}))
    content = forms.CharField(label="Content", widget=forms.Textarea(attrs={'class' : 'form-control col-md-6'}))

def index(request):
    if request.method == "POST":
        search_item = request.POST.get("q")
        if(util.get_entry(search_item) is not None):
            return entry(request,search_item)
        else:
            search_list=[]
            for en in util.list_entries():
                if search_item.lower() in en.lower():
                    search_list.append(en)
            return render(request, "encyclopedia/index.html", {
                "entries": search_list
                })

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request,entry):
    file = util.get_entry(entry)
    M=Markdown()
    if file is None:
        return render(request,"encyclopedia/notfound.html")
    else:
        return render(request,"encyclopedia/All_entry.html",{
            "content":M.convert(file),
            "name":entry
        })


def newpage(request):
    Flag = False
    if request.method == "POST":
        data = Newformnewpage(request.POST)
        if data.is_valid():
            title_data = data.cleaned_data["title"]
            content_data = data.cleaned_data["content"]
            if util.get_entry(title_data) is None or data.cleaned_data["editform"]:
                util.save_entry(title_data, content_data)
                return entry(request,title_data)
            else:
                Flag = True
                return render(request, "encyclopedia/newpage.html", {
                    "form":data,
                    "Flag":Flag,
                    "entry":title_data,
                    "edit": False
                })
        else:
            Flag = True
            return render(request, "encyclopedia/newpage.html", {
                "form": data,
                "Flag": Flag,
                "entry": data.cleaned_data["title"],
                "edit":False
            })


    return render(request, "encyclopedia/newpage.html" ,{
        "form":Newformnewpage() ,
        "Flag":Flag
    })

def edit(request, entry):
    if util.get_entry(entry) is None:
        return render(request, "encyclopedia/notfound.html")
    else:
        F = Newformnewpage()
        F.fields["title"].initial = entry
        F.fields["title"].widget = forms.HiddenInput()
        F.fields["content"].initial = util.get_entry(entry)
        F.fields["editform"].initial = True
        return render(request,"encyclopedia/newpage.html",{
            "form":F,
            "Flag":False,
            "edit":True,
            "entry": entry
        })

def random(request):
    from random import randint
    all_entry = util.list_entries()
    entry = randint(0,len(all_entry)-1)
    return HttpResponseRedirect(reverse("wiki:entry", kwargs= {'entry' : all_entry[entry]}))

