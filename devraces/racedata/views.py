from django.shortcuts import render

# Create your views here.

from rest_framework import generics
from django.http import HttpResponse, JsonResponse
from racedata.models import Pilot
import datetime
from racedata.serializers import PilotSerializer
from django.db.utils import IntegrityError
import copy


class PostData(generics.RetrieveUpdateDestroyAPIView):

    def delete(self, request, *args, **kwargs):
        Pilot.objects.all().delete()
        return JsonResponse('Todos los datos han sido eliminados',
                     status=201, safe=False)


    def post(self, request, *args, **kwargs):

        point_ref=[25,18,15,12,10,8,6,4,2,1]

        times = []
        dtimes = []
        laptimes=[]

        for pilot in request.data:

            pilot_times=[]
            pilot_dtimes = []
            pilot_laptimes = []
            for race in pilot['races']:
                laps=[int(lap['time'][0:2])*3600+int(lap['time'][3:5])*60+float(lap['time'][6:]) for lap in race['laps']]
                secs=sum(laps)
                best_lap=min(laps)
                pilot_times.append(secs)
                pilot_dtimes.append(str(datetime.timedelta(seconds=secs)))
                pilot_laptimes.append(str(datetime.timedelta(seconds=best_lap)))

            times.append(pilot_times)
            dtimes.append(pilot_dtimes)
            laptimes.append(pilot_laptimes)

        points = copy.deepcopy(times)
        position = copy.deepcopy(times)

        for race in range(len(times[0])):
            competitors=[i[race] for i in times]
            sorted_competitors = sorted(competitors)
            ppos = [sorted_competitors.index(pilot) for pilot in competitors]
            ppoints=[point_ref[i] if i < 10 else 0 for i in ppos]

            for i in range(len(ppoints)):
                points[i][race]=ppoints[i]
                position[i][race] = ppos[i]+1


        p_ind=0
        for pilot in request.data:

            pname=pilot['name']
            pid=pilot['_id']
            ppicture=pilot['picture']
            page = pilot['age']
            pteam = pilot['team']
            ptotal_pts = sum(points[p_ind])
            ptotal_time=str(datetime.timedelta(seconds=sum(times[p_ind])))

            praces = {}
            r_ind=0
            for race in pilot['races']:

                praces[race['name']]={'Posición': position[p_ind][r_ind],'Puntos':points[p_ind][r_ind], 'Tiempo Total':dtimes[p_ind][r_ind], 'Mejor Vuelta':laptimes[p_ind][r_ind]}
                r_ind+=1

            p_ind+=1

            try:
                newP=Pilot(name=pname,idcode=pid,picture=ppicture,age=page,team=pteam,races=str(praces), total_pts=ptotal_pts, total_time=ptotal_time)
                newP.save()
            except IntegrityError:
                return JsonResponse(
                    'Los datos introducidos ya están presentes en la base de datos',status=201, safe=False)


        return JsonResponse('¡Datos guardados! '+str(len(competitors))+ ' pilotos en '+str(len(times[0]))+' carreras', status=201, safe=False)



class GetPilot(generics.RetrieveUpdateDestroyAPIView):

    def get(self, request, *args, **kwargs):

        if len(Pilot.objects.all())==0:
            return HttpResponse('ERROR: No hay ningún piloto en la base de datos')

        if request.query_params.get('name')==None:
            return HttpResponse('ERROR: El parámetro "name" no se encuentra en la request')

        try:
            mypilot=Pilot.objects.get(name=request.query_params.get('name'))
            dict={"Nombre":mypilot.name,"ID":mypilot.idcode,"Edad":mypilot.age,"Equipo":mypilot.team,"Foto":mypilot.picture,"Carreras":eval(mypilot.races)}
        except TypeError:
            return HttpResponse('ERROR: El parámetro "name" no se encuentra en la request')
        except Pilot.DoesNotExist:
            return HttpResponse('ERROR: El piloto "' +request.query_params.get('name')+'" no se encuentra en la base de datos')

        return JsonResponse(dict, status=201)


class GetRace(generics.RetrieveUpdateDestroyAPIView):

    def get(self, request, *args, **kwargs):

        if len(Pilot.objects.all())==0:
            return HttpResponse('ERROR: No hay ningún piloto en la base de datos')
        classification=[0]*len(Pilot.objects.all())
        race=request.query_params.get('name')

        if race==None:
            return HttpResponse('ERROR: El parámetro "name" no se encuentra en la request')

        for pil in Pilot.objects.all():
            try:
                dict=eval(pil.races)[race]
                classification[dict['Posición']-1]={'Nombre':pil.name, 'Datos de su carera':dict}
            except Pilot.DoesNotExist:
                pass
            except KeyError:
                return HttpResponse('ERROR: La carrera no se encuentra en la base de datos')

        return JsonResponse(classification, status=201, safe=False)


class AllRacesList(generics.ListAPIView):
    queryset = Pilot.objects.all()
    serializer_class = PilotSerializer