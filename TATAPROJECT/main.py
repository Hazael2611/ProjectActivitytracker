from log import open_log
from mainwindow import showmain_window


if __name__=="__main__":
#call open_log function from log.py and send showmain_window from mainwindow.py as its parameter to execute both and initialize the program
    open_log(showmain_window)  



"""
NEXT STEPS:

implementarle IA para que los tips sean personalizados dependiendo la informacion trackeada

Que no sea local, sobre todo la base de datos, que sea una app mobil

Hacer un modelo de machine learning, con los datos de estado de animo y los minutos de actividad fisica
determinar si esa persona va a dejar de hacer ejercicio y le mande tips o mensajes motivacionales asi como el progreso logrado
"""


#prmp, modificar si es monthly or weekly

"""
Prompt=f" You are an expert from health sector, give a tip for the user, the tip could be information of 
health in general, specific for the sport that the user practice the most, how to increase user's perform in the sport, mental heath tips
if the minutes done by the user are a few give a motivation advice or tips to start and if the minutes done are too much give rest tips.
The data from the user are listed below, the data recorded is per month
mintues done {} 
sports that the user practice {} and intensity {}
strees {} where 1 is nothing and 10 is too much
sleep quality {}  where 1 is nothing and 10 is too much
motivation {} where 1 is nothing and 10 is high
if the user feels satisfied with his physical activity: {}
if the user feel difficulty to stay motivated:{}
"

 dstart, dlength, comeback_day = dropoutdays()
       # abandono
      #  if drstart <= day < dstart + dlength:
       #     continue
        #if comeback_day and day < comeback_day and day >= drop_start + drop_length:
         #   continue
"""