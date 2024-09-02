from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK,
                                   HTTP_404_NOT_FOUND,
                                   HTTP_500_INTERNAL_SERVER_ERROR,
                                   HTTP_201_CREATED,
                                   HTTP_403_FORBIDDEN)
from .models import Board
from .serializers import BoardSerializer
from rest_framework.exceptions import PermissionDenied
from Task.serializers import TaskSerializer
from django.db import models
from User.models import User


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def BoardView(request, **kwargs):
    if request.method == 'GET':
        if 'pk' in kwargs:
            try:
                pk = kwargs.get('pk')
                board = Board.objects.get(pk=pk)
                if (not request.user in board.users) or (request.user != boards.author):
                    raise PermissionDenied
                board = BoardSerializer(board).data
                return Response({
                    'status': 'success',
                    'data': {
                        'board': board
                    }
                }, status=HTTP_200_OK)
            except Board.DoesNotExist:
                return Response({
                    'status': 'error',
                    'message': 'Not found'
                }, status=HTTP_404_NOT_FOUND)
            except PermissionDenied:
                return Response({
                    'status': 'fail',
                    'message': 'User is not authorized'
                }, status=HTTP_403_FORBIDDEN)
            except Exception:
                return Response({
                    'status': 'error',
                    'message': 'Internal server error'
                }, status=HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            try:
                boards = Board.objects.all()
                filtered_boards = []

                for board in boards:
                    filtered_tasks = [task for task in board.tasks.all() if task.author == request.user or request.user in task.users.all()]
                    if filtered_tasks:
                        board.filtered_tasks = filtered_tasks
                        filtered_boards.append(board)

                boards = []
                for board in filtered_boards:
                    board_data = BoardSerializer(board).data
                    board_data['tasks'] = TaskSerializer(board.filtered_tasks, many=True).data
                    boards.append(board_data)

                return Response({
                    'status': 'success',
                    'data': {
                        'boards': boards
                    }
                }, status=HTTP_200_OK)

            except Exception as error:
                return Response({
                    'status': 'error',
                    'message': 'Internal server error'
                })

    if request.method == 'POST':
        try:
            user = request.user
            board = Board.objects.create(
                title=request.data.get('title'),
            )

            board = BoardSerializer(board).data

            return Response({
                'status': 'success',
                'data': {
                    'board': board
                }
            }, status=HTTP_201_CREATED)

        except Exception as error:
            print(error)
            return Response({
                'status': 'error',
                'message': 'Internal server error'
            }, status=HTTP_500_INTERNAL_SERVER_ERROR)

    if request.method == 'DELETE':
        try:
            pk = kwargs.get('pk')
            board = Board.objects.get(pk=pk)
            if board.author != request.user:
                raise PermissionDenied

            board.delete()

            return Response(status=HTTP_200_OK)

        except Board.DoesNotExist:
            return Response({
                'status': 'fail',
                'message': 'Board not found'
            }, status=HTTP_404_NOT_FOUND)
        except PermissionDenied:
            return Response({
                'status': 'fail',
                'message': 'User is not authorized'
            }, status=HTTP_403_FORBIDDEN)
        except Exception as error:
            return Response({
                'status': 'error',
                'message': 'Internal server error'
            }, status=HTTP_500_INTERNAL_SERVER_ERROR)
