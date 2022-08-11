import socketio
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from django.shortcuts import render
from .forms import PatientData, HNArray, HNTextField

sio = socketio.AsyncServer(async_mode='asgi')
background_task_started = False
patientdataset = formset_factory(PatientData, can_delete=True, max_num=10, absolute_max=1000)
hnformset = formset_factory(HNArray, can_delete=True, max_num=10, absolute_max=1000)


@login_required(login_url='signin')
def index(request):
    return render(request, 'socketio.html')


"""
HN (Hospital number) to PID (personal/patient identification number)
TXN (Transaction number) to VID (visit identification number)
SER (Serial number of item) to IID (item identification number)
"""


@login_required(login_url='signin')
def patient_page(request):
    hntext = HNTextField()
    hndataform = hnformset(prefix='hn', auto_id=True)
    return render(request, 'patient.html', {'hntext': hntext, 'hndataform': hndataform})


# As Join room to ensure that only current HN will be collected.

@sio.on('patient')  # sio.on('patient', HN)
async def patient(sid, message):  # Receive only HN
    # sio.enter_room(sid, message['hn'])
    print(message)
    await sio.emit('hn_response', {
        'data': message,
        # 'data': 'HN: ' + message['hn'] + ' Date of Birth: ' + message['birthdate'] + ' Gender: ' + message['gender'],
        # 'register': message['register']
    }, room=sid)
    data = list()
    register = True
    # Querying by HN
    # Patient data (HN) >> Upsert HN >> PID
    """
    # data should be looked like this
    data = [
        {"HN": "01234", "birthDate": "1987-06-05", "gender": True},
        {"HN": "56789", "birthDate": "2000-12-31", "gender": False},
    ]
    """
    await sio.emit('patient_next', {data, register}, room=sid)


@login_required(login_url='signin')
def visit_page(request):
    return render(request, 'visit.html')


#    return render(request, 'visit.html', {'patientdataform': patientdataform})


@sio.on('connect')
async def test_connect(sid, environ):
    await sio.emit('response', {'data': 'Connected to Database'}, room=sid)


# Visit data (HN, TXN) >> Transform >> PID, TXN >> Upsert TXN >> PID, VID
@sio.on('visit')
async def visit(sid, message):
    await sio.emit('txn_response', {'data': message['txn']}, room=message['hn'])


# Item data (HN, TXN, SER) >> Transform >> PID, VID, IID
@sio.on('item')
async def item(sid, message):
    await sio.emit('ser_response', {'data': message['ser'] + ' of ' + message['txn']}, room=message['hn'])


@sio.on('leave')
async def leave(sid, message):
    sio.leave_room(sid, message['hn'])
    await sio.emit('response', {'data': 'Left room: ' + message['hn']}, room=sid)


@sio.on('close')
async def close(sid, message):
    await sio.emit('response', {'data': 'HN ' + message['hn'] + ' is closing.'}, room=message['hn'])
    await sio.close_room(message['hn'])


# echo
@sio.on('event')
async def test_message(sid, message):
    await sio.emit('response', {'data': message['data']}, room=sid)


# @sio.on('connect')
# async def test_connect(sid, environ):
#   await sio.emit('response', {'data': 'Connected'}, room=sid)


@sio.on('disconnect request')
async def disconnect_request(sid):
    await sio.disconnect(sid)


@sio.on('disconnect')
def test_disconnect(sid):
    print('Client disconnected')
