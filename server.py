"""Local/LAN HTTP and WebSocket relay for Core Drillers. Not a hardened public service."""
import argparse
import asyncio
import json
import re
import secrets
import time
from pathlib import Path
from aiohttp import web, WSMsgType

ROOT = Path(__file__).resolve().parent
rooms = {}

async def index(request):
    return web.FileResponse(ROOT / 'index.html')

async def send(ws, data):
    if not ws.closed:
        await ws.send_json(data)

async def publish(room, msg, exclude=None):
    await asyncio.gather(*(send(p['ws'], {'op':'event', 'msg':msg}) for pid,p in list(room['people'].items()) if pid != exclude), return_exceptions=True)

def roster(room):
    return [{'id':pid,'name':p['name'],'cls':p['cls'],'bot':False} for pid,p in room['people'].items()] + room['bots']

async def socket(request):
    ws = web.WebSocketResponse(heartbeat=25, max_msg_size=524288)
    await ws.prepare(request)
    pid = secrets.token_hex(8)
    code = None
    window = time.monotonic()
    count = 0
    try:
        async for item in ws:
            if item.type != WSMsgType.TEXT:
                continue
            now = time.monotonic()
            if now-window > 1:
                window, count = now, 0
            count += 1
            if count > 240:
                await ws.close(code=1008, message=b'Rate limit')
                break
            try:
                m = json.loads(item.data)
            except (ValueError, TypeError):
                continue
            if not isinstance(m, dict):
                continue
            op = m.get('op')
            if op == 'ping':
                await send(ws, {'op':'pong','time':m.get('time')})
            elif op in ('host','join') and code is None:
                candidate = str(m.get('code','')).strip().upper()
                if not re.fullmatch(r'[A-Z0-9]{3,12}', candidate):
                    await send(ws, {'op':'error','why':'Invalid room code'})
                    continue
                if op == 'host':
                    if candidate in rooms:
                        await send(ws, {'op':'error','why':'Room already exists'})
                        continue
                    rooms[candidate] = {'host':pid,'people':{},'bots':[],'started':False}
                room = rooms.get(candidate)
                if not room or room['started'] or len(room['people']) >= 4:
                    await send(ws, {'op':'error','why':'Room unavailable, full, or already launched'})
                    continue
                code = candidate
                room['bots'] = room['bots'][:max(0,3-len(room['people']))]
                room['people'][pid] = {'ws':ws,'name':str(m.get('name','Crew'))[:32], 'cls':str(m.get('cls','miner'))[:24]}
                await send(ws, {'op':'ready','id':pid,'code':code,'roster':roster(room)})
                await publish(room, {'t':'roster','roster':roster(room)})
            elif code and code in rooms:
                room = rooms[code]
                if op == 'profile':
                    room['people'][pid].update(name=str(m.get('name','Crew'))[:32], cls=str(m.get('cls','miner'))[:24])
                    await publish(room, {'t':'roster','roster':roster(room)})
                elif op == 'msg' and isinstance(m.get('msg'),dict):
                    msg = dict(m['msg'])
                    t = msg.get('t')
                    host_only = {'st','start','roster','kill','wallbreak','dgate','orestate'}
                    if t in host_only and pid != room['host']:
                        continue
                    if t == 'roster':
                        proposed = msg.get('roster',[])
                        if not isinstance(proposed,list):
                            continue
                        room['bots'] = [b for b in proposed if isinstance(b,dict) and b.get('bot')][:max(0,4-len(room['people']))]
                        msg['roster'] = roster(room)
                    if t == 'start':
                        room['started'] = True
                        msg['roster'] = roster(room)
                    msg['_from'] = pid
                    if t == 'p':
                        msg['id'] = pid
                    await publish(room, msg, exclude=pid)
    finally:
        if code and code in rooms:
            room = rooms[code]
            room['people'].pop(pid, None)
            if pid == room['host']:
                rooms.pop(code,None)
                await asyncio.gather(*(p['ws'].close(code=1001,message=b'Host left') for p in room['people'].values()), return_exceptions=True)
            else:
                await publish(room, {'t':'roster','roster':roster(room)})
    return ws

def make_app():
    app = web.Application(client_max_size=524288)
    app.router.add_get('/', index)
    app.router.add_get('/index.html', index)
    app.router.add_get('/ws', socket)
    return app

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host',default='127.0.0.1',help='Use 0.0.0.0 for trusted LAN access')
    parser.add_argument('--port',type=int,default=8080)
    args = parser.parse_args()
    web.run_app(make_app(),host=args.host,port=args.port)
