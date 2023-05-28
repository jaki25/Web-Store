from typing import Any, Dict
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.shortcuts import render
from .models import Store, Article, Type_Article
from django.views.generic import ListView, DetailView
from django.views import View
from django.core.mail import send_mail
from django.contrib.sessions.models import Session
from django.utils import timezone
# Create your views here.


#Client side

#Main page for client side. Show all store and direction for store page
class MainPageView(ListView):
    template_name="bmdSite/main.html"
    model=Store

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context["stores"]=Store.objects.all()
        return context
        
#Store view. Shows all article from the Store.
class StoreView(View):
    

    def get(self, request, slug):
        
        store= Article.objects.filter(store__slug=slug).exclude(quantity__lte=1)
        
        context={
            "store_slug":slug,
            "store_name":store.first().store.name,
            "store":store
        }
        
        return render(request, "bmdSite/store.html", context)
    
    def post(self, request, slug):

        quantity=1
        if request.method=="POST":
            item_checked=request.session.get("item_checked")
        
        
        #check is the item already initialized
        if item_checked is None:
            item_checked={}
            print("usao u prvi if \n")

        article_id=int(request.POST["article_id"])
        
        print("this is ID %d" %article_id)
        temp_article= Article.objects.get(id=article_id)
        slug=temp_article.store.slug

        if str(article_id) not in list(item_checked.keys()):
            item_checked[str(article_id)]=quantity
            #item_checked.append(article_id)
            print(quantity)
            
            print(article_id)
            request.session["item_checked"]=item_checked
            print(request.session["item_checked"])
            #objasniti
            request.session.modified=True
            
       
            
        
        return HttpResponseRedirect("/store"+slug)


#making session for every article to be stored in the box 

class BoxView(View):
    
#list all article from the session
    def get(self, request):
        price_total=0
        if "item_checked" in request.session:
            item_checked=request.session.get("item_checked")
            
        else:
            item_checked=None
        context={}
        
        #if there is no data
        if item_checked is None or len(item_checked)==0:

            context["articles"]=[]
            context["has_something"]=False
        else:
            
            temp_dict1={} #dict for showing quantity per article id
            temp_dict2={} #dict for showing total_price per item

            for article_id, quantity in item_checked.items():
                article_Id=int(article_id)
                       
                print("this is quantity %d" %quantity)         
                temp_dict1[article_Id]=quantity
                print("article %d quantity %d" %(int(article_id), quantity))
             
                context["has_something"]=True
                
                price_per_item=Article.objects.get(id=article_Id).type_arttcle.price*quantity
                price_total+=price_per_item

                temp_dict2[article_Id]=price_per_item

                context["price_total_item"]=temp_dict2
                context["price_total"]=price_total

            context["quantity"]=temp_dict1   
            article=Article.objects.filter(id__in=item_checked)
            context["articles"]=article

        return render(request, "bmdSite/box.html", context)
    

#create session if it is not created yet, and save the article into it.
    def post(self, request):
        print("usao u post requesT")
        item_checked=request.session.get("item_checked")
        
        print(request.POST)    
        #The button delete is clicked
        if "delete_article" in request.POST:
            article_id=int(request.POST["article_id"])
            del item_checked[str(article_id)]
            
            request.session["item_checked"]=item_checked
            
            return HttpResponseRedirect("/box")
        

        # the button submit (buy) whole page is clicked
        elif "buy_articles" in request.POST:
            context={}
            articles=Article.objects.filter(id__in=item_checked)
            email=request.POST["user_email"]
            phone_num=request.POST["phone_num"]
            total_price=str(request.POST["total_price"])
            print("kupi artickle")
            context["total_price"]=total_price
            context["email"]=email
            context["phone"]=phone_num
            messages=""
            for article in articles:
                messages+=f'{article.type_arttcle.name} (Cijena:{article.type_arttcle.price})'
            subject='Potvrda o uspijesnoj kupovini'
            message=f'{messages} Ukupna cijena racuna:{total_price}'
            from_email= "kostarasovic25@gmail.com"
            to_email=[from_email,email]
            send_mail(subject,message,from_email,to_email,fail_silently=False)
            
            delete_session(request)
        


        return  render(request, "bmdSite/success.html",context)

#Add to session

def Add_to_session(request):
    if request.method=="POST":
        item_checked=request.session["item_checked"]
        
        print("usao u dodaj kolicinu")
        kljuc=request.POST["kljuc"]
        quantity=request.POST["vrijednost"]

        item_checked[kljuc]=int(quantity)
        
        print(kljuc, quantity)
        request.session["item_checked"]=item_checked

    return HttpResponse('OK') #reverse("box-page")

def delete_session(request):
    session_key=request.session.session_key
    if not session_key:
        return
    
    try:
        session=Session.objects.get(session_key=session_key)
    except Session.DoesNotExist:
        return
    
    session_data = session.get_decoded()
    for key in session_data:
        del request.session[key]

    request.session.save()