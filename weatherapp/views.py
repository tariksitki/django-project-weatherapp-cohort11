from django.shortcuts import render, get_object_or_404, redirect
## pythonda api ye istek icin:  bunu önce install etmek gerekir.
import requests
from django.contrib import messages
from .models import City
### gelen veriyi daha güzel okumak icin:
from pprint import pprint
# apikey .env dosyasinda
from decouple import config



def index(request):
    API_KEY = config("API_KEY")
    city = "Yozgat"

    ## user in form ile girdigi sehir:
    u_city = request.POST.get("name")  ## input un name i name oldugu icin
    print(u_city)

    if u_city:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={u_city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        print(response.ok)  ## eger user in yazdigi isimde api de veri varsa ok True 

        ## ### user in search ile girdigi sehir ismi var ise db ye kaydedecegiz:
        ## user in girdigi isimde db ye kaydedilebilir yada gelen veri icinde cekilir:
        if response.ok:
            content = response.json()
            r_city = content["name"]
            if City.objects.filter(name = r_city):
                messages.warning(request, "City already exist")
            else:
                City.objects.create(name=r_city) 

        else:  ### api de böyle bir sehir yok. 
            messages.warning(request, "There is no city")

    city_data = []  # herbir istekte degisecegi icin list e atiyoruz. 
        ## her bir istekte api den tek sehir cekebiliyoruz. Bu nedenle tüm isimler icin ayri bir istek gönderiyoruz.     
    cities = City.objects.all()  ## query set  
    for city in cities:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        content = response.json()
        data = {
            # "name": content["name"],
            "name": city,  ## id kullanabilmek icin template de böyle yaptik. api den id gelmez. bize kendi db mizdeki verilerin id si lazim template icin. 
            "temp": content["main"]["temp"],
            "description": content["weather"][0]["description"],
            "icon": content["weather"][0]["icon"],
        }
        city_data.append(data)
        print(city)


    
    
    response = requests.get(url)
    content = response.json()  # json formatindaki veriyi python dict e dönüstürür
    # print("---------------------")
    # print(response)
    # pprint(content)
    # pprint(content["name"])  ## print ettigimizde görürüz bizim isimize bu veri yarayacak
    # pprint(content["main"]["temp"])
    # pprint(content["weather"][0]["description"])
    # pprint(content["weather"][0]["icon"])

        ## verilerimizi öncelikle terminalde inceledik sonra context icine attik. 
    context = {
        # "name": content["name"],
        # "temp": content["main"]["temp"],
        # "description": content["weather"][0]["description"],
        # "icon": content["weather"][0]["icon"],
        "city_data" : city_data
    }


    return render(request, 'weatherapp/index.html', context)

## sicaklik bize kelvin olarak gelir. Bunu url sonuna parametre koyarak degistiririz
### units=metric"








def delete_city(request, id):
    # city = City.objects.get(id=id) ## normalde böyle yapiyoruz. ama bu sehri bulamazsa anlamsiz bir hata return eder. 
    city = get_object_or_404(City, id=id)  
                                # bu daha kullanisli
                                ## model doesn't exist hatasi yerine Http404 hatasi döndürür. hatalarin kullanici dostu olmasi lazim. o nedenle bu daha kullanisli. docs a baktigimizda normalde bu algoritma try except ile kurulu. ama bu kod hem hatayi hem de saglam kisminda ne yapacagini icerir. 
    city.delete()
    messages.success(request, "City deleted")
    return redirect("home")

    