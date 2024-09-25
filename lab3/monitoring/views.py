from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from .serializers import *
from .models import Request, Threat, RequestThreat
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import logout
from datetime import datetime 


class ThreatList(APIView):
    model_class = Threat
    serializer_class = ThreatListSerializer

    # получить список угроз
    def get(self, request):
        threats = self.model_class.objects.all()
        serializer = self.serializer_class(threats, many=True)
        return Response(serializer.data)

class ThreatDetail(APIView):
    model_class = Threat
    serializer_class = ThreatDetailSerializer

    # получить описание угрозы
    def get(self, request, pk):
        threat = get_object_or_404(self.model_class, pk=pk)
        serializer = self.serializer_class(threat)
        return Response(serializer.data)
    

    # удалить угрозу (для модератора)
    def delete(self, request, pk):

        if not request.user.is_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)

        threat = get_object_or_404(self.model_class, pk=pk)
        threat.status = 'deleted'
        threat.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    # добавить новую угрозу (для модератора)
    def post(self, request, format=None):

        if not request.user.is_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # обновление угрозы (для модератора)
    def put(self, request, pk, format=None):

        if not request.user.is_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)

        threat = get_object_or_404(self.model_class, pk=pk)
        serializer = self.serializer_class(threat, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 

class AddThreatView(APIView):
    # добавление услуги в заявку
    def post(self, request):
        # создаем заявку, если ее еще нет
        if not Request.objects.filter(user=request.user,status='draft').exists():
            new_req = Request()
            new_req.user = request.user
            new_req.save()
            
        request_id = Request.objects.filter(user=request.user,status='draft').first().pk
        serializer = RequestThreatSerializer(data=request.data)
        if serializer.is_valid():
            new_req_threat = RequestThreat()
            new_req_threat.threat_id = serializer.validated_data["threat_id"]
            new_req_threat.request_id = request_id
            if 'price' in request.data:
                new_req_threat.price = request.data["price"]
            new_req_threat.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

# TODO
class ImageView(APIView):
    def post(self, request):
        if not request.user.is_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)

        return Response({}, status=status.HTTP_400_BAD_REQUEST)
    


# USER VIEWS
class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# Личный кабинет (обновление профиля)
class UserUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = UserUpdateSerializer(instance=request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Аутентификация пользователя
class UserLoginView(APIView):
    def post(self, request):
        serializer = AuthTokenSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Деавторизация пользователя
class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()  # Удаляем токен
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)
    



# Модераторы
class ListRequests(APIView):
    def post(self, request):

        if not request.user.is_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = CheckUsernameSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(username=serializer.validated_data['username'])
            requests = Request.objects.filter(user=user).exclude(status='draft').exclude(status='deleted')
            req_serializer = RequestSerializer(requests,many=True)
            return Response(req_serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class GetRequests(APIView):
    
    def get(self, request, pk):
        req = get_object_or_404(Request, pk=pk)
        serializer = RequestSerializer(req)

        threat_requests = RequestThreat.objects.filter(request=req)
        threats_ids = []
        for threat_request in threat_requests:
            threats_ids.append(threat_request.threat_id)

        threats_in_request = []
        for id in threats_ids:
            threats_in_request.append(get_object_or_404(Threat,pk=id))

        threats_serializer = ThreatListSerializer(threats_in_request,many=True)
        response = serializer.data
        response['threats'] = threats_serializer.data

        return Response(response,status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        serializer = PutRequestSerializer(data=request.data)
        if serializer.is_valid():
            req = get_object_or_404(Request, pk=pk)
            for attr, value in serializer.validated_data.items():
                setattr(req, attr, value)
            req.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class FormRequests(APIView):
    def put(self, request, pk):
        req = get_object_or_404(Request, pk=pk)
        if not req.status=='draft':
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if not request.user == req.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        if req.created_at > datetime.now():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if not req.ended_at == None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        req.formed_at = datetime.now()
        req.status = 'formed'
        req.save()
        return Response(status=status.HTTP_200_OK)
    

class ModerateRequests(APIView):
    def put(self,request,pk):

        if not request.user.is_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)

        req = get_object_or_404(Request, pk=pk)
        serializer = AcceptRequestSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.validated_data['accept'] == True:
                req.status = 'accepted'
                req.moderator = request.user

                # calc final price
                threat_requests = RequestThreat.objects.filter(request=req)

                final_price = 0

                for threat_request in threat_requests:
                    final_price = final_price + threat_request.price

                req.final_price = final_price
            else:
                req.status = 'declined'
                req.moderator = request.user 
                req.ended_at = datetime.now()
            req.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        

    def delete(self, request, pk):
        if not request.user.is_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)
        req = get_object_or_404(Request, pk=pk)
        req.status = 'deleted'
        req.save()
        return Response(status=status.HTTP_200_OK)
    

class EditRequestThreat(APIView):
    def delete(self, request, pk):
        if 'threat_id' in request.data:
            record = get_object_or_404(RequestThreat, request=pk,threat=request.data['threat_id'])
            record.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
    def put(self,request,pk):
        if not request.user.is_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)
        if 'threat_id' in request.data and 'price' in request.data:
            record = get_object_or_404(RequestThreat, request=pk,threat=request.data['threat_id'])
            record.price = request.data['price']
            record.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
