from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_201_CREATED
from Task.models import Task, Subtask
from Task.serializers import TaskSerializer, SubtaskSerializer
from Board.models import Board
from User.models import User


@api_view(http_method_names=['GET', 'POST'])
@permission_classes([IsAuthenticated])
def TaskView(request, **kwargs):
    if request.method == 'GET':
        if 'pk' in kwargs.keys():
            try:
                pk = kwargs.get('pk')
                task = Task.objects.get(id=pk)
                task = TaskSerializer(task).data
                return Response({
                    'status': 'success',
                    'data': {
                        'task': task
                    }
                }, status=HTTP_200_OK)
            except Task.DoesNotExist:
                return Response({
                    'status': 'error',
                    'message': 'Not found'
                }, status=HTTP_404_NOT_FOUND)
            except Exception:
                return Response({
                    'status': 'error',
                    'message': 'Internal Server Error'
                }, status=HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            try:
                tasks = Task.objects.all()
                tasks = TaskSerializer(tasks, many=True).data

                return Response({
                    'status': 'success',
                    'data': {
                        'tasks': tasks
                    }
                }, status=HTTP_200_OK)
            except Exception as error:
                return Response({
                    'status': 'error',
                    'message': error
                })

    if request.method == 'POST':
        try:
            board   = Board.objects.get(pk=request.data.get('board_id'))
            users   = User.objects.filter(pk__in=request.data.get('users'))

            task = Task(
                title=request.data.get('title'),
                body=request.data.get('body'),
                author=request.user,
                deadline=request.data.get('deadline'),
                status=request.data.get('status'),
            )

            task.save()
            board.tasks.add(task)
            task.users.set(users)
            task = TaskSerializer(task).data

            return Response({
                'status': 'success',
                'data': {
                    'task': task
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
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Not found'
            }, status=HTTP_404_NOT_FOUND)
        except Exception:
            return Response({
                'status': 'error',
                'message': 'Internal server error'
            }, status=HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'POST', 'DELETE', 'PUT'])
@permission_classes([IsAuthenticated])
def SubtaskView(request, **kwargs):
    if request.method == 'GET':
        if 'pk' in kwargs:
            try:
                pk = kwargs.get('pk')
                subtask = Subtask.objects.get(pk=pk)
                subtask = SubtaskSerializer(subtask).data

            except Subtask.DoesNotExist:
                return Response({
                    'status': 'error',
                    'message': 'Subtask not found'
                }, status=HTTP_404_NOT_FOUND)

            except Exception:
                return Response({
                    'status': 'error',
                    'message': 'Internal Server Error'
                }, status=HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            try:
                subtasks = Subtask.objects.all()
                subtasks = SubtaskSerializer(subtasks, many = True).data

                return Response({
                    'status': 'success',
                    'data': {
                        'subtasks': subtasks
                    }
                })
            except Exception:
                return Response({
                    'status': 'error',
                    'message': 'Internal Server Error'
                }, status=HTTP_500_INTERNAL_SERVER_ERROR)

    if request.method == 'POST':
        try:
            task = Task.objects.get(pk=request.data.get('task'))

            subtask = Subtask.objects.create(
                body=request.data.get('body'),
                is_completed=False
            )

            subtask.save()

            task.subtasks.add(subtask)
            task.save()

            subtask = SubtaskSerializer(subtask).data

            return Response({
                'status': 'success',
                'data': {
                    'subtask': subtask
                }
            }, status=HTTP_201_CREATED)

        except Exception as error:
            print(error)
            return Response({
                'status': 'error',
                'message': 'Internal Server Error'
            }, status=HTTP_500_INTERNAL_SERVER_ERROR)

    if request.method == 'DELETE':
        try:
            subtask = Subtask.objects.get(pk=pk)
            task = Task.objects.filter(subtask in subtasks)

            task.subtasks.remove(subtask)

            task.save()
            subtask.delete()

        except Exception as error:
            return Response({
                'status': 'error',
                'message': 'Internal Server Error'
            })
